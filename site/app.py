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

  for item in islice(i, size):
    yield item
  
  other = sum(item[1] for item in i)
  if other > 0:
    yield label, other


def top(items, size=5):
  return slice(items, size, "DESC")

def bottom(items, size=5):
  return slice(items, size, "ASC")


def sort(iter, col, dir="ASC"):
  if dir == "ASC":
    reversed = False
  elif dir == "DESC":
    reversed = True

  return sorted(iter, key=lambda r:r[col], reverse=reversed)

def sorted_query(db, q_str, col=1):
  return sort(query(db, q_str), col=col)

def ensure_dir(path):
  dirname = os.path.dirname(path)
  if not os.path.exists(dirname):
    os.makedirs(dirname)


@app.before_first_request
def open_db():
  if __name__ == "__main__" and len(sys.argv) > 1:
    fname = sys.argv[1]
  else:
    # fetch some data from s3
    conn = boto.connect_s3(
      os.environ['AWS_KEY'],
      os.environ['AWS_SECRET']
    )
    bucket = conn.get_bucket('com.mozillalabs.blink')

    item = iter(bucket.list('data/reduce:')).next()
    fname = os.path.join(
      os.environ['DATA_DB_PATH'],
      str(item.key)
    )
    if not os.path.exists(fname):
      ensure_dir(fname)
      item.get_contents_to_filename(fname)
    
  app.db = DiscoDB.load(open(fname))


@app.template_filter('value')
def value(k):
  return k.split(':',1)[-1]

@app.template_filter('commas')
def commas(val):
  return "{:,d}".format(val)

@app.route('/')
def index():
  q = request.args.get('q')
  if q:
    results =  sorted_query(app.db, q)
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
    app.run(
      debug=True
    )