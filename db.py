import math
import string
import inspect
import json
import ast
import operator

from collections import namedtuple
from functools import partial
from itertools import islice, count, groupby

from discodb import DiscoDB
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

    self.select('*')
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


  def select(self,cols="*"):
    if cols:
      if cols == '*':
        cols = ','.join(self.__schema__)

      self.col_exps = codd.parse(
        "({})".format(cols), 
        get_value=self.get_value
      ).func_closure[0].cell_contents


      #self.col_exps = [
      #  codd.parse(col, get_value=self.get_value)
      #  for col in cols
      #]

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
      'udf': self.udfs()
    }

    table = (
      self.project(_load_value(record), ctx)
      for record in self
    )

    results = self.order(self.group(table),self.ordering)
    return results[self.start:self.stop]

  def udfs(self):
    def str_func(f):
      def _(s,*args):
        if s is None:
          return None
        else:
          return f(s,*args)
      return _

    functions = dict(
      set((n, str_func(f)) for n,f in inspect.getmembers(string, inspect.isfunction)) |
      set(inspect.getmembers(math, inspect.isbuiltin))
    )

    functions['split_part'] = str_func(lambda s,delim, field: s.split(delim)[field] )

    functions.update(self.aggregates)

    return functions

  def __iter__(self):
    return self.filter(self.records)



  def project(self, record, ctx):
    return  self.result_class(*[col(record, ctx) for col in self.col_exps])

  def group_by(self, *grouping):
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


  def _order_key(self, attr, direction="desc"):
    direction = direction.lower()
    get_key = codd.parse(attr)

    if direction == "desc":
      return get_key
    elif direction == "asc":
      def invert(record, ctx):
        value = get_key(record,ctx)
        v_type = type(value)
        # TODO: utilize types if/when we get them
        if v_type in (int, float, long, complex):
          return -value
        elif v_type  in ( str,  bytearray):
          return [-b for b in bytearray(value)]
        elif v_type == unicode:
          return [-b for b in bytearray(value.encode('utf-8'))]
        else:
          return None
      return invert
    else:
      raise RuntimeError("direction must be DESC or ASC")

  def _key_fun(self,*cols):
    order_key = self._order_key

    ordering  = [
      order_key(*c.rsplit(None,1)) for c in cols
    ]

    def key_fun_(record):
      return [key(record, None) for key in ordering]

    return key_fun_


  def order_by(self, *cols):
    self.ordering = cols
    return self


  def order(self, table, cols):
    if not cols:
      return list(table)
    else:
      return sorted(table, key=self._key_fun(*cols))



def disco_query(op):
  query = query_from(op)

  def filter(db):
    return (
      doc
      for docid in db.query(query)
      for doc in db[docid]
    )

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
    return  ikey(attr, value_exp(op.comparators[0]))
  elif comp_op == ast.NotEq:
    return "(*{} & ~{})".format(attr, ikey(attr, value_exp(op.comparators[0])))
  elif comp_op == ast.In:
    return "|".join([ "*" + ikey(attr,v) for v in value_exp(op.comparators[0])]) 

def ikey(key,value):
  return "{}:{}".format(key,value) 
 

def value_exp(op):
  t = type(op)
  return {
    ast.Num: int_exp,
    ast.Str: str_exp,
    ast.Tuple: tuple_exp,
    ast.Name: none_exp
  }[t](op)


def int_exp(op):
  return op.n

def str_exp(op):
  return op.s

def tuple_exp(op):
  return map(value_exp, op.elts)

def none_exp(op):
  assert op.id == 'None'
  return None

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



