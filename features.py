from datetime import datetime

import codd
from splicer import Schema

from urlparse import urlparse, urljoin
from urlnorm import norm as urlnorm
import json
from collections import Counter

def size(doc):
  """Returns size of the payload"""
  kilobytes = len(doc['payload']) / 1024
  yield 'size_in_kilobytes', kilobytes

def host(doc):
  """Returns the host for the given doc"""
  p = urlparse(doc['url'])
  yield "host", p.hostname
  yield "scheme", p.scheme

def header(doc):
  yield 'headers', [dict(name=k, value=v) for k,v in doc['headers'].items()]

  #for header, value in doc['headers'].items():
  #  yield "header:{}".format(header), value

def timestamp(doc):
  tstamp = doc['headers'].get('x_commoncrawl_FetchTimestamp')
  if tstamp:
    tstamp = datetime.fromtimestamp(int(tstamp)/1000).isoformat()
  yield "timestamp", tstamp

def content_type(doc):
  """Returns contexnt_type:xxx"""
  yield 'content_type', doc.get('content_type')


def tag_attr(tag, attr, feature=None):
  """Returns a function useful for extracting a single non missing value from a tag"""
  if feature is None:
    feature = tag

  def _(doc):
    if doc.has_key('dom'):
      for element in doc['dom'].find_all(tag):
        value = element.get(attr)
        if value:
          yield value
  _.__name__ = feature
  return _

def tags(doc):
  """
  Extracts each tag name from the document preserving it's hiearchy
  """
  dom = doc.get('dom')
  if dom:
    counts = Counter((
      t.name 
      for t in dom.descendants 
      if hasattr(t,'name') and t.name 
    ))

    yield "tags", [dict(name=k, count=v) for k,v in counts.iteritems()]
 

def absolute_link(tag, attr, feature=None):
  """Extract a url from a tag returning it's absolute name.

  """

  url_from = tag_attr(tag, attr, feature)
  
  def u_norm(doc_url, url):
    try:
      return urlnorm(urljoin(doc_url,url))
    except:
      return "invalid:" + url


  def _(doc):
    doc_url = doc['url']

    yield feature, [
      u_norm(doc_url, url)
      for url in url_from(doc)
    ]

  _.__name__ = url_from.__name__
  return _

def outbound():
  links = absolute_link('a', 'href')
  def _(doc):
    doc_url = doc['url']
    doc_loc = urlparse(doc_url).netloc

    yield "link_to", filter( 
      lambda link_loc:  link_loc != doc_loc,
      [
        urlparse(url).netloc
        for feature, urls in links(doc)
        for url in urls
      ]
    )

  _.__name__ = "link_to"
  return _


scripts   = absolute_link('script', 'src', 'scripts')
css      = absolute_link('link', 'href', 'css')


methods = [
  size,
  host,
  content_type,
  scripts,
  outbound(),
  css,
  header,
  timestamp,
  tags
]

schema = Schema([
  dict(name="size_in_kilobytes", type="INTEGER"),
  dict(name="host", type="STRING"),
  dict(name="content_type", type="STRING"),
  dict(name="scripts", type="STRING", mode="REPEATED"),
  dict(name="css", type="STRING", mode="REPEATED"),
  dict(name="link_to", type="STRING", mode="REPEATED"),
  dict(
    name="headers", 
    type="RECORD", 
    mode="REPEATED",
    fields=[
      dict(
        name="name",
        type="string"
      ),
      dict(
        name="value",
        type="string"
      )
    ],
   ),
  dict(name="timestamp", type="DATETIME"),
  dict(
    name="tags", 
    type="RECORD", 
    mode="REPEATED",
    fields=[
      dict(
        name="name",
        type="string"
      ),
      dict(
        name="count",
        type="INTEGER"
      )
    ],
  ),
  dict(name="scheme", type="STRING")
])


names    = [m.__name__ for m in methods]
names.append('scheme')
features = codd.parallel(*methods)

def docid(params):
  # TODO: need code similar to this if/when we run multiple workers
  #doc_count = params['doc_counter'] = params.get('doc_count',0)
  #return (doc_count * params['worker_count']) + params['worker_id']
  if not hasattr(params, 'doc_count'):
    params.doc_count = 0
  params.doc_count += 1
  return params.doc_count

def default(schema):
  """Given a schema return the default record"""

  return {
    f.name: [] if f.mode == "REPEATED" else None
    for f in schema.fields
  }

def setfield(record, field, value):
  if field.mode == "REPEATED":
    if type(value) in (list, set):
      record[field.name].extend(value)
    else:
      record[field.name].append(value)


  else:
    record[field.name]=value

def index_field(field, value, root=''):

  if field.mode == 'REPEATED':
    if field.type == 'RECORD':
      indexer = index_repeating_record
    else:
      indexer = index_repeating_scalar
  else:
    if field.type == 'RECORD':
      indexer = index_record
    else:
      indexer = index_scalar

  return indexer(field, value, root)

def index_scalar(field, value, root):
  yield "{}{}".format(root, field.name), value

def index_repeating_scalar(field, value, root):
  return (
    (k,v)
    for item in value
    for k,v in index_scalar(field, item, root)
  )

def index_repeating_record(field, value, root):
  return (
    (k, v)
    for item in value
    for k,v in index_record(field, item, root) 
  )

def index_record(field, value, root):
  
  subroot = "{}{}.".format(root, field.name)

  for subfield in field.fields:
    for subkey, subvalue in index_field(subfield, value[subfield.name], subroot):
      #print "{} -->{}".format(subkey, subvalue)
      yield subkey, subvalue


def extractor(doc, params):
  doc_id = docid(params)
  
  # ->(doc_id, http://..)
  #yield "{}".format(doc_id), doc['url']
  


  record = default(schema)

  for feature, value in features(doc):
    #attrs[feature] = value
    field = schema[feature]
    setfield(record, field, value)

    for key, value in index_field(field,value):
      try:
        key = str("%s=%s" % (feature,value))
        yield key, doc_id
      except Exception, e:
        yield "error:{}".format(e), doc_id

  yield "{}".format(doc_id), json.dumps(record)
