from nose.tools import *
import bs4

from . import TestCase

import features
from splicer import Field

def doc(content, url="http://example.com/folder1/somedoc.html"):
  return dict(
    url = url,
    dom = bs4.BeautifulSoup(content),
    payload = content
  )

class TestFeatureExtractors(TestCase):

  def test_scripts(self):
    content =  """
    <html>
    <body>
      <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js"></script>
      <script src="http://ajax.googleapis.com/ajax/libs/chrome-frame/1.0.3/CFInstall.min.js">
    </body>
    </html>"""

    doc_features =  list(features.scripts(doc(content)))
    eq_(
      doc_features,
      [
        (
          'scripts', 
          [
            u'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js', 
            u'http://ajax.googleapis.com/ajax/libs/chrome-frame/1.0.3/CFInstall.min.js'
          ]
        )
      ]
    )

  def test_links(self):
    content = """
    <html>
    <body>
      <a href="http://blah.com">blah</a>
      <a href="../relative/./link">Hi mom</a>
    </body>
    </html>
    """
    f = features.outbound()
    doc_features = list(f(doc(content)))
    self.assertSequenceEqual(
      doc_features,
      [
        ('link_to', ['blah.com']),
      ]
    )

  def test_tags(self):
    content = """
    <html>
    <body>
      <a href="http://blah.com">blah</a>
      <a href="../relative/./link">Hi mom</a>
      <div id="1">
        <span></span>
        <div>
          <ul>
           <li>One</li>
           <li>Two</li>
          </ul>
        </div>
      </div>
    </body>
    </html>
    """
    doc_features = list(features.tags(doc(content)))

    self.assertSequenceEqual(
      doc_features,
      [
        (
          'tags',
          [
            {'count': 1, 'name': u'body'},
            {'count': 2, 'name': u'a'},
            {'count': 1, 'name': u'span'},
            {'count': 2, 'name': u'li'},
            {'count': 1, 'name': u'ul'},
            {'count': 1, 'name': u'html'},
            {'count': 2, 'name': u'div'}
          ]
        )
      ]
    )
   
  def test_index_scalar(self):
    field = Field(name="count", type="INTEGER")

    results = list(features.index_scalar(field, 2, ''))
    
    assert_sequence_equal(
      results,
      [('count',2)]
    )


  def test_index_repeating_scalar(self):
    field = Field(name="count", type="INTEGER", mode="REPEATED")

    results = list(features.index_repeating_scalar(field, [1,2,3], ''))
    
    assert_sequence_equal(
      results,
      [
        ('count',1),
        ('count',2),
        ('count',3)
      ]
    )

  def test_index_record(self):
    field = Field(
      name="point", 
      type="RECORD",
      fields=[
        dict(name="x", type="INTEGER"),
        dict(name="y", type="INTEGER")
      ]
    )

    results = list(features.index_record(field, dict(x=10,y=1), ''))
    
    assert_sequence_equal(
      results,
      [
        ('point.x',10),
        ('point.y',1)
      ]
    )

  def test_repeating_index_record(self):
    field = Field(
      name="point", 
      type="RECORD",
      mode="REPEATED",
      fields=[
        dict(name="x", type="INTEGER"),
        dict(name="y", type="INTEGER")
      ]
    )

    results = list(features.index_repeating_record(field, [dict(x=1,y=1), dict(x=2,y=2)], ''))
    
    assert_sequence_equal(
      results,
      [
        ('point.x',1),
        ('point.y',1),
        ('point.x',2),
        ('point.y',2)
      ]
    )