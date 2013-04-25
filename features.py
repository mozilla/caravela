import codd
from urlparse import urlparse

def size(doc):
  """Returns size of the payload"""
  kilobytes = len(doc['payload']) / 1024
  yield 'size', "{} k".format(kilobytes)

def host(doc):
  """Returns the host for the given doc"""
  yield "host", urlparse(doc['url']).hostname

def header(doc):
  for header, value in doc['headers'].items():
    yield "header:{}".format(header), value

def content_type(doc):
  """Returns contexnt_type:xxx"""
  yield 'content_type', doc.get('content_type')


def attr(tag, attr, feature=None):
  if feature is None:
    feature = tag

  def _(doc):
    if doc.has_key('html'):
      for element in doc['html'].find_all(tag):
        value = element.get(attr)
        if value:
          yield feature, value
  _.__name__ = feature
  return _


def script(doc):
  if doc.has_key('html'):
    for element in doc['html'].find_all('script'):
      src = element.get('src')
      if src:
        yield 'script', src

def link(doc):
  if doc.has_key('html'):
    for element in doc['html'].find_all('a'):
      link =  element.get('href')
      if link:
        yield 'link', link

methods = [
  size,
  host,
  content_type,
  attr('script', 'src'),
  attr('a', 'href', 'outbound'),
  attr('link', 'href', 'css'),
  header
]

names = [m.__name__ for m in methods]
names.append('doc_id')

features      = codd.parallel(*methods)

def docid(params):
  #doc_count = params['doc_counter'] = params.get('doc_count',0)
  #return (doc_count * params['worker_count']) + params['worker_id']
  if not hasattr(params, 'doc_count'):
    params.doc_count = 0
  params.doc_count += 1
  return params.doc_count

def extractor(doc, params):
  doc_id = docid(params)
  
  # ->(doc_id, http://..)
  yield "{}".format(doc_id), doc['url']

  for feature, value in features(doc):
    try:
      yield str("%s:%s" % (feature,value)), doc_id
    except Exception, e:
      yield "error:{}".format(e), doc_id
