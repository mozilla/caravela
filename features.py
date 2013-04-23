import codd
from urlparse import urlparse

def size(doc):
  """Returns size of the payload"""
  yield 'size', len(doc['payload'])

def host(doc):
  """Returns the host for the given doc"""
  yield "host", urlparse(doc['url']).hostname


def content_type(doc):
  """Returns contexnt_type:xxx"""
  yield 'content_type', doc.get('content_type')

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
  script,
  link
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
  
  yield "doc_id:{}".format(doc_id), doc['url']

  for feature, value in features(doc):
    try:
      yield str("%s:%s" % (feature,value)), doc_id
    except Exception, e:
      yield "error:{}".format(e), doc_id
