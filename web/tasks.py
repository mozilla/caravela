import os
import sys
from datetime import timedelta
from urlparse import urlparse
from itertools import islice
from functools import partial
import time
import json
import errno

import boto
from celery import Celery
from celery.utils.log import get_task_logger
from celery.task import periodic_task
from celery.task.schedules import crontab
from celery.task import periodic_task

from discodb import DiscoDB, DiscoDBError


from splicer.compilers.local import is_aggregate
from splicer.ast import GroupByOp, Var, Function, SliceOp


import db

from filelock import FileLock, FileLockException


celery = Celery('tasks', backend='amqp', broker=os.environ['BROKER_URL'])
logger = get_task_logger(__name__)

# start crying wolf if lock exists longer
# than this time in seconds
MAX_LOCK_AGE = 10 * 60

state = dict(
  count=0,
  cache_time = 0,
  max_cache_age = 60 * 5,
  dbs = {}
) 

def ensure_dir(path):
  dirname = os.path.dirname(path)
  if not os.path.exists(dirname):
    os.makedirs(dirname)

def progress(fname, downloaded, size):
  logger.info("Downloaded %s of %s to %s", downloaded, size, fname)

@periodic_task(run_every=timedelta(minutes=10), time_limit=530)
def sync_dbs():

  # prevent multiple workers on the same box from
  # synching the directory at the same time
  lock_path = os.path.join(os.environ['DATA_DB_PATH'], 'tmp/db.lock')
  ensure_dir(lock_path)

  try:
    with FileLock(lock_path, wait=False):
      download_dbs()
  except FileLockException:
    logger.warn("Lockfile %s exists skiping sync",lock_path)

@periodic_task(run_every=timedelta(minutes=1))
def lock_watch():

  lock_path = os.path.join(os.environ['DATA_DB_PATH'], 'tmp/db.lock')
  try:
    age = time.time() - os.path.getctime(lock_path)
  except OSError as e:
    if e.errno == errno.ENOENT:
      return
    else:
      raise

  if age > MAX_LOCK_AGE:
    logger.warn("Lockfile %s is older that max age, investigate and remove",lock_path)


def download_dbs():
  # fetch some data from s3
  conn = boto.connect_s3(
    os.environ['AWS_KEY'],
    os.environ['AWS_SECRET']
  )
  data_db_path = os.environ['DATA_DB_PATH']
  tmp_path     = os.path.join(data_db_path, 'tmp')
  url          = urlparse(os.environ['BUCKET_URL'])
  bucket       = conn.get_bucket(url.hostname)
  s3_root      = url.path[1:]
  s3_root_len  = len(s3_root)

  for item in bucket.list(s3_root):
    if item.key.endswith('/'):
      # skip directory place holder
      continue

    fname = os.path.join(
      data_db_path,
      str(item.key[s3_root_len:])
    )
    tmp_name = os.path.join(
      tmp_path,
      str(item.key[s3_root_len:])
    )

    if not os.path.exists(fname):
      logger.info('Downloading %s', fname)
      ensure_dir(tmp_name)
      item.get_contents_to_filename(tmp_name,cb=partial(progress, fname))
      os.rename(tmp_name, fname)


def cached_db(state):
  """
  Open the database
  """
  if time.time() - state['cache_time'] > state['max_cache_age']:
    scan_database_dir(state)
  return state['dbs'].values()[0] if state['dbs'].values() else None


def scan_database_dir(state):
  db_path = os.environ['DATA_DB_PATH']
  for fname in (os.path.join(db_path, f) for f in os.listdir(db_path)):
    if fname not in state['dbs'] and os.path.isfile(fname):
      try:
        state['dbs'][fname] = DiscoDB.load(open(fname))
      except DiscoDBError:
        # maybe a corrupt discodb, nuke it the sync
        # process should fetch a new one later on
        os.remove(fname)
        logger.exception('Unable to open %s', fname)

  if state['dbs']:
    state['cache_time'] = time.time()
  return state


@celery.task()
def relations():
  dataset = db.init(docs=cached_db(state))
  return [(name, schema.to_dict()) for name, schema in dataset.relations]


@celery.task()
def schema(relation_name):
  dataset = db.init(docs=cached_db(state))
  return dataset.get_schema(relation_name).to_dict()

@celery.task()
def query(statement):
  dataset = db.init(docs=cached_db(state))
  query = dataset.query(statement)

  if not isinstance(query.operations, SliceOp):
    query = dataset.frm(query).limit(100)


  result = query.execute()

  return json.dumps(dict(
    schema=[f.name for f in result.schema.fields],
    records=list(result)
  ))



@celery.task()
def execute(cols=None, where=None, limit=100, offset=0, order_by=[]):
  """select header"""


  dataset = db.init(docs=cached_db(state))
  query = dataset.frm('docs')

  if cols:
    query = query.select(cols)


  # query contains aggregate expresions, automatically add
  # group_by columns
  group_by = query.operations
  if isinstance(group_by, GroupByOp):
    exprs =  group_by.relation.exprs
    names = []
    for e in exprs:
      if isinstance(e,Var):
        names.append(e.path)
      elif isinstance(e, Function):
        if not is_aggregate(e, dataset):
          names.append(e.name)
    query = query.group_by(','.join(names))

  if where:
    query = query.where(where)

  if order_by:
    query = query.order_by(order_by)




  query = query.limit(limit).offset(offset)
  return json.dumps(dict(
    schema=[f.name for f in query.schema.fields],
    records=list(query)
  ))



@celery.task()
def ticks():
  return state['count']


if sys.argv[0].endswith('celeryd'):
  # start
  sync_dbs.delay()
  pass