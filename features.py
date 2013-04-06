import codd

def size(doc):
  """Returns size:xxx"""
  yield 'size', len(doc.text)


def content_type(doc):
  """Returns contexnt_type:xxx"""
  return 'content_type', doc.get('content_type')

def scripts(doc):
  for element in doc.find_all('script'):
    yield 'script', element.get('src')

def links(doc):
  for element in doc.find_all('a'):
    yield 'links', element.get('href')

#features = codd.parallel(
#  size,
#  content_type,
#  scripts,
#  links
#)

def docid(params):
  doc_count = params['doc_counter'] = params.get('doc_count',0)
  return (doc_count * params['worker_count']) + params['worker_id']

def extrator(doc, params):
  doc_id = docid(params)
  
  yield "doc_id:{}".format(doc_id), doc['url']

  for feature, value in features(doc):
    yield "%s:%s" % (k,v), doc_id 
