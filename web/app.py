import os
import sys
import json

from flask import (
  Flask, 
  render_template, 
  make_response,
  request,  
  jsonify
)

from . import tasks


app = Flask(__name__)


def sort(iter, col, dir="ASC"):
  if dir == "ASC":
    reversed = False
  elif dir == "DESC":
    reversed = True

  return sorted(iter, key=lambda r:r[col], reverse=reversed)

def execute(q_str, col=1):
  results = tasks.count.delay(q_str).get()
  return sort(results, col=col)

def ensure_dir(path):
  dirname = os.path.dirname(path)
  if not os.path.exists(dirname):
    os.makedirs(dirname)

@app.template_filter('value')
def value(k):
  return k.split(':',1)[-1]

@app.template_filter('commas')
def commas(val):
  return "{:,d}".format(val)

@app.route('/')
def index():
  return render_template(
    'index.html',
    features = execute("*feature", col=0),
  )


@app.route('/spec/')
@app.route('/spec/<path:query>')
def spec(query='*feature'):
  """Generate a vega spec file from query"""

  table = dict(
    name="table",
    values =  [
      dict(x=x, y=y) 
      for x,y in
      execute(query)
    ]
  )
   

  response =  make_response(render_template(
    'spec.json', 
    data = json.dumps([table])
  ))
  response.headers['content-type'] = "application/json"
  return response
  

@app.route('/json')
def json_endpoint():
  # move column parsing to the db module

  cols = filter(None,request.args.get('cols','').split(','))

  limit = int(request.args.get('limit',100))
  results = tasks.execute.delay(cols=cols,limit=limit).get()
  response = make_response(results)
  response.headers['content-type'] = "application/json"

  return response

@app.route("/insights")
def list_insights():
  return jsonify(insights=list(insights.all()))

@app.route("/insights/<id>")
def get_insight(id):
  return jsonify(insight=insights.get(id))

from . import insights