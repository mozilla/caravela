from discodb import DiscoDB
from collections import namedtuple
from functools import partial
import json
import ast
from itertools import islice, count, groupby
import operator

import codd


_key        = str
_value      = json.dumps
_load_key   = int
_load_value = json.loads

class DB(object):
  def __init__(self, records):
    if isinstance(records, DiscoDB):
      self.records = records

      # todo: rebuild discodbs with meta data
      self.schema = list(records['feature'])
      self.record_count = len(records.query('*scheme'))

    else:
      schema = sorted(set(
        k
        for r in records
        for k in r.keys()
      ))

      self.schema = schema
      self.records = DiscoDB(self.index(records))

      self.record_count  = len(records)

    self.__schema__ = self.schema

    self.aggregates = {
      "count": aggregate(
        function=lambda state: state + 1,
        initial=0
      )

    }

    self.select(*self.__schema__)
    self.start = 0
    self.stop = self.record_count
    
    self.grouping = []
    self.ordering = []



  def create_aggregate(self, name, function, initial=None, finalize=None):
    self.aggregates[name] = aggregate(function, initial, finalize)

  def index(self, records):
    # store a series of dicts in disco db

    for doc_id, record in enumerate(records):
      doc_id = _key(doc_id+1)
      yield doc_id, _value(record)
      for field in self.schema:
        yield "{}:{}".format(field, record[field]), doc_id


  def get_value(self, attr):
    """Returns a function that will retrive the value of an 
    attribute from a record.

    codd normally retrievs the values from the attr of the object
    we're using dictionaries.
    """
    def getter(row, ctx):
      return row.get(attr)
    return getter


  def select(self,*cols):
    if cols:
      
      self.col_exps = [
        codd.parse(col, get_value=self.get_value)
        for col in cols
      ]

      self.reducers = [
        (pos, self.aggregates[col.__name__])
        for pos, col in enumerate(self.col_exps)
        if col.__name__ in self.aggregates
      ]
 
      self.schema = [
        getattr(c, '__name__', "col{}".format(i))
        for i,c in enumerate(self.col_exps)
      ]
      result_class = self.result_class = namedtuple("row", self.schema)

    return self

  def where(self, clause):
    op = ast.parse(clause).body[0].value
    # op is an instance of an allowed class

    assert any(isinstance(op,cls) for cls in (ast.BoolOp, ast.Compare))
    self.filter = disco_query(op)

    return self

  def limit(self, limit):
    self.stop = limit
    return self

  def offset(self, offset):
    self.start = offset
    return self


  def filter(self,db):
    """
    Returns a generatr over  all raw records
    """
    # discodb returns a DiscoDBInquiry for d[key]
    # this unwraps it
    return (
      doc
      for docid in xrange(0, self.record_count)
      for doc in db[str(docid + 1)]
    )


  def execute(self, *params):
    ctx = {
      'params': params,
      'udf': self.aggregates
    }
    table = (
      self.project(_load_value(record), ctx)
      for record in self
    )

    results = self.order(self.group(table),self.ordering)
    return results[self.start:self.stop]


  def __iter__(self):
    return self.filter(self.records)



  def project(self, record, ctx):
    return  self.result_class(*[col(record, ctx) for col in self.col_exps])

  def groupby(self, *grouping):
    self.grouping = grouping
    return self

  def group(self, table):
    if not self.reducers:
      # no aggergates, no work
      return table


    if len(self.reducers) == len(self.schema):
      # Returning nothing but aggregated values, reduce
      # the whole table without groups
      return [self.aggregate(None, table)]
    else:
      if self.grouping:
        grouping = self.grouping
      else:
        grouping = [
          c.__name__
          for c in self.col_exps
          if c.__name__ not in self.aggregates
        ]

      # optimization hint.. we create 2x temporary tuples
      # here one for the sort the other for the groupby
      return (
        self.aggregate(group, values)
        for group, values in groupby(
          self.order(table, grouping),
          key=operator.attrgetter(*grouping)
        )
      )

  def aggregate(self, group, records):

    def reduction(states, record, reducers=self.reducers):
      for pos, reducer in reducers:
        state = states[pos]
        args = record[pos]

        states[pos] = reducer.function(state, *args)

      return states

    first_record = records.next()
    initial = list(first_record)
    for pos, reducer in self.reducers:
      initial[pos] = reducer.initial
    initial = reduction(initial, first_record)

    return self.result_class(*reduce(reduction, records, initial))


  def order(self, table, cols):
    if not cols:
      return list(table)
    else:
      return sorted(table, key=operator.attrgetter(*cols))



def disco_query(op):
  query = query_from(op)

  def filter(db):
    return db.query(query)
  return filter


def query_from(op):
  if isinstance(op, ast.Compare):
    return compare_exp(op)
  else:
    return bool_exp(op)


def compare_exp(op):
  """Returns a function for selecting doc ids and filtering"""

  # curious if we'll ever hit this
  assert len(op.ops) == 1, "Not sure, why this would have multiple ops" 
  assert isinstance(op.left, ast.Name)
  assert len(op.comparators) == 1

  comp_op = type(op.ops[0])
  attr = op.left.id
  if comp_op == ast.Eq:

    return "*" + ikey(attr, value_exp(op.comparators[0]))
  elif comp_op == ast.In:
    return "|".join([ "*" + ikey(attr,v) for v in value_exp(op.comparators[0])]) 

def ikey(key,value):
  return "{}:{}".format(key,value) 
 

def value_exp(op):
  t = type(op)
  return {
    ast.Num: int_exp,
    ast.Str: str_exp,
    ast.Tuple: tuple_exp
  }[t](op)


def int_exp(op):
  return op.n

def str_exp(op):
  return op.s

def tuple_exp(op):
  return map(value_exp, op.elts)

def bool_exp(op):

  t = type(op.op)
  if t == ast.And:
    sep = " & "
  elif t == ast.Or:
    sep = " | "

  return "(" + sep.join(query_from(o) for o in op.values) + ")"


class aggregate(object):
  def __init__(self, function, initial=None, finalize=None):
    self.function = function
    self.initial = initial
    self.finalize = finalize
    self.state = None

  def __call__(self, *args):
    return args



