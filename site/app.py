import os
import sys
from functools import partial
from itertools import islice, chain

from discodb import DiscoDB
import boto
from flask import Flask, render_template, request, g


app = Flask(__name__)


def count(iter):
  return sum(1 for _ in iter)

def query(db, q_str):
  if q_str:
    for subquery, values in db.metaquery(q_str):
      yield str(subquery), count(values)

# expects list to be sorted
def slice(items, size, dir, label="Other"):
  if dir == "ASC":
    i = iter(items)
  elif dir == "DESC":
    i = reversed(items)
  else:
    raise ValueError("dir must be ASC|DESC")

  s     = islice(i, size)
  other = label, sum(item[1] for item in i)

  # note other is always last regardless of it's
  # value... not sure if that's proper or not
  if dir == "ASC":
    return chain(s, (other,))
  else:
    return chain(reversed(s), (other,))

def top(items, size=5):
  return slice(items, size, "DESC")

def bottom(items, size=5):
  return slice(items, size, "ASC")

def value((k,count)):
  return k.split(':',1)[1], count


def sort(iter, col, dir="ASC"):
  if dir == "ASC":
    reversed = False
  elif dir == "DESC":
    reversed = True

  return sorted(iter, key=lambda r:r[col], reverse=reversed)

def sorted_query(db, q_str, col=1):
  return sort(query(db, q_str), col=col)

@app.before_first_request
def open_db():
  if len(sys.argv > 1):
    fname = sys.arv[1]
  else:
    # fetch some data from s3
    conn = boto.s3_connectection(
      os.environ['AWS_KEY'],
      os.environ['AWS_SECRET']
    )
    bucket = conn.get_bucket('com.mozillalabs.blink')

    bucket = conn.bucket('blink')
    item = bucket.list('data/').next()
    fname = os.path.join(
      os.environ['DATA_DB_PATH'],
      str(item.key)
    )
    if not os.path.exists(fname):
      item.get_contents_to_path(fname)

  app.db = DiscoDB.load(open(fname))



@app.template_filter('commas')
def commas(val):
  return "{:,d}".format(val)

@app.route('/')
def index():
  q = request.args.get('q')
  if q:
    results = [ value(item) for item in sorted_query(app.db, q)]
  else:
    results = []

  return render_template(
    'index.html', 
    features = sorted_query(app.db, "*feature", col=0),
    results = results,
    sort = sort,
    top = top,
    bottom = bottom
  )

if __name__ == '__main__':
    app.run(debug=True)