from datetime import datetime

import codd
from urlparse import urlparse, urljoin
from urlnorm import norm as urlnorm
import json
from collections import Counter

def size(doc):
  """Returns size of the payload"""
  kilobytes = len(doc['payload']) / 1024
  yield 'size', "{} k".format(kilobytes)

def host(doc):
  """Returns the host for the given doc"""
  p = urlparse(doc['url'])
  yield "host", p.hostname
  yield "scheme", p.scheme

def header(doc):
  for header, value in doc['headers'].items():
    yield "header:{}".format(header), value

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
          yield feature, value
  _.__name__ = feature
  return _

def tag(doc):
  """
  Extracts each tag name from the document preserving it's hiearchy
  """
  dom = doc.get('dom')
  if dom:
    counts = Counter((
      t.name 
      for t in dom.descendants 
      if hasattr(t,'name') 
    ))

    for k,v in counts.iteritems():
      yield 'tag', "{}:{}".format(k,v)

    return
      

  if dom:
    for t in dom.descendants:
      if hasattr(t, 'name'):
        yield 'tag', t.name
        # <div><span></span></div> -> (div, div:span)
        #import pdb; pdb.set_trace()
        #hiearchy = [p.name for p in t.parents][:-1]
        #hiearchy.insert(0,t.name)
        #yield 'tag', '>'.join(reversed(hiearchy)) 
     
  


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

    return (
      (feature, u_norm(doc_url, url))
      for feature, url in url_from(doc)
    )
  _.__name__ = url_from.__name__
  return _

def outbound():
  links = absolute_link('a', 'href')
  def _(doc):
    doc_url = doc['url']
    doc_loc = urlparse(doc_url).netloc
    for tagname, url in links(doc):
      link_loc = urlparse(url).netloc
      if link_loc and doc_loc != link_loc:
        yield 'link_to', link_loc
  _.__name__ = "link_to"
  return _


script   = absolute_link('script', 'src')
css      = absolute_link('link', 'href', 'css')


methods = [
  size,
  host,
  content_type,
  script,
  outbound(),
  css,
  header,
  timestamp,
  tag
]



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

def extractor(doc, params):
  doc_id = docid(params)
  
  # ->(doc_id, http://..)
  #yield "{}".format(doc_id), doc['url']

  attrs = {}
  for feature, value in features(doc):
    attrs[feature] = value
    try:
      yield str("%s:%s" % (feature,value)), doc_id
    except Exception, e:
      yield "error:{}".format(e), doc_id

  yield "{}".format(doc_id), json.dumps(attrs)
