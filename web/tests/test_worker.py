import os
import shutil
import tempfile
from unittest import TestCase

from discodb import DiscoDB

from nose.tools import eq_
from web import tasks

class TestDBWrapper(TestCase):


  def setUp(self):
    self._old_db_path = os.environ['DATA_DB_PATH']
    self.tmp_dir = os.environ['DATA_DB_PATH'] = tempfile.mkdtemp()
    
  def tearDown(self):
    shutil.rmtree(self.tmp_dir)
    os.environ['DATA_DB_PATH'] = self._old_db_path

  def create_db(self, name, data):
    db_path = os.path.join(os.environ['DATA_DB_PATH'], name + '.db')
    data = DiscoDB(data)
    data.dump(open(db_path, 'w'))
    return db_path
  

  def test_scan_database_dir(self):
    state = dict(
      dbs={},
    )

    db_path = self.create_db(
      'test',
      [("A", "1"), ("A", "2"), ("B","1")]
    )

    state = tasks.scan_database_dir(state)

    assert db_path in state['dbs']

    # scan_database_dir should remove invalid databases if
    # it encounters them  
    invalid_path = os.path.join(os.environ['DATA_DB_PATH'],'invalid.db')
    open(invalid_path,'w').write('1234')

    state = tasks.scan_database_dir(state)

    assert db_path in state['dbs']
    assert invalid_path not in state['dbs']
    assert not os.path.exists(invalid_path)

  def test_cached_db(self):
    state = dict(
      dbs={},
      cache_time = 0,
      max_cache_age = 10 * 60
    )

    # no database, cached_db should return None
    assert tasks.cached_db(state) is None
    

    db_path = self.create_db(
      'test',
      [("A", "1"), ("A", "2"), ("B","1")]
    )

    assert tasks.cached_db(state)
    assert db_path in state['dbs']

