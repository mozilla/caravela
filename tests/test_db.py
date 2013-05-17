from db import DB
from discodb import DiscoDB

from nose.tools import eq_

from . import TestCase
import datetime

class TestDB(TestCase):
  def setUp(self):

    self.db = DB([
      dict(
        name="John",
        login_count=2 
      ),
      dict(
        name="Bob",
        login_count=1
      )
    ])

  def test_select_all(self):
    self.assertSequenceEqual(
      self.db.select().execute(),
      [
        (2, "John"),
        (1,"Bob")
      ]
    )

  def test_select_name(self):
    self.assertSequenceEqual(

      self.db.select('name').execute(),
      [
        ("John",),
        ("Bob",)
      ]
    )

  def test_create_aggregate(self):

    self.db.create_aggregate(
      name="bogus",
      function=lambda state: state + 1,
      initial=0
    )
    
    self.db.select("count()")
    eq_(len(self.db.reducers),1)


    self.db.select("name", "count()")
    eq_(len(self.db.reducers),1)

    self.db.select("count()", "bogus(login_count)")
    eq_(len(self.db.reducers),2)





  def test_select_count(self):
    self.assertSequenceEqual(
      self.db.select('count()').execute(),
      [
        (2,),
      ]
    )


  def test_select_col_with_count(self):

    self.assertSequenceEqual(
      self.db.select('name','count()').groupby("name").execute(),
      [
        ('Bob',1),
        ('John', 1)
      ]
    )

  def test_where(self):
    self.assertSequenceEqual(
      self.db.where("login_count == 2").execute(),
      [
        (2, "John")
      ]
    )

  def test_select_where(self):
    self.assertSequenceEqual(
      self.db.select("login_count").where("name == 'John'").execute(),
      [
        (2, )
      ]
    )

  def test_select_where_and(self):
    self.assertSequenceEqual(
      self.db.select("login_count").where("name == 'John' and login_count == 2").execute(),
      [
        (2, )
      ]
    )

  def test_where_or(self):
    self.assertSequenceEqual(
      self.db.where("name == 'John' or login_count == 1").execute(),
      [
        (2, "John"),
        (1,"Bob")
      ]
    )

  def test_where_in(self):
    self.assertSequenceEqual(
      self.db.where("login_count in (1,2)").execute(),
      [
        (2, "John"),
        (1,"Bob")
      ]
    )





