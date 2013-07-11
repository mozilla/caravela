from db import DB
from discodb import DiscoDB

from nose.tools import eq_


from . import TestCase
import datetime

class TestDB(TestCase):
  def setUp(self):

    self.db = DB(
      [
        dict(
          name="John",
          login_count=2 
        ),
        dict(
          name="Bob",
          login_count=1
        )
      ],
      schema=dict(
        fields=[
          dict(
            name="name",
            type="STRING"
          ),
          dict(
            name="login_count",
            type="INTEGER"
          )

        ]
      )
    )

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


    self.db.select("name, count()")
    eq_(len(self.db.reducers),1)

    self.db.select("count(), bogus(login_count)")
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
      self.db.select('name,count()').group_by("name").execute(),
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

    self.assertSequenceEqual(
      self.db.where("login_count != 1").execute(),
      [
        (2, "John")
      ]
    )

    self.assertSequenceEqual(
      self.db.where("login_count != None").execute(),
      [
        (2, "John"),
        (1, "Bob")
       
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

  def test_order_key(self):
    get_key=self.db._order_key("blah")
    ctx = None

    class int_attr:
      blah = 1

    class str_attr:
      blah = "foo"

    class dict_attr:
      blah = {}

    eq_(get_key(int_attr, ctx), 1)
    eq_(get_key(str_attr, ctx), 'foo')
    eq_(get_key(dict_attr,ctx), {})

    get_key=self.db._order_key("blah", "asc")
    eq_(get_key(int_attr, ctx), -1)
    eq_(get_key(str_attr, ctx), [-b for b in bytearray('foo')])
    eq_(get_key(dict_attr, ctx), None)

    get_key=self.db._order_key("blah", "DeSc")
    eq_(get_key(int_attr, ctx), 1)
    eq_(get_key(str_attr, ctx), 'foo')
    eq_(get_key(dict_attr, ctx), {})


  def test_order_by(self):
    self.assertSequenceEqual(
      self.db.order_by("name").execute(),
      [
        (1,"Bob"),
        (2, "John")
      ]
    )

  def test_order_by_asc(self):
      self.assertSequenceEqual(
        self.db.order_by("name ASC").execute(),
        [
          (2, "John"),
          (1,"Bob")
        ]
      )

  def test_multiple_order_by_asc(self):
    #TODO: this test needs more data to prove it's correctness
    self.assertSequenceEqual(
      self.db.order_by("login_count","name ASC").execute(),
      [
        (1,"Bob"),
        (2, "John"),
       
      ]
    )







