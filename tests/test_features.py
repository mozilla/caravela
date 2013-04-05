from nose.tools import eq_
import bs4

from . import TestCase

import features



class TestFeatureExtractors(TestCase):

  def test_scripts(self):
    content =  """
    <html>
    <body>
      <script src="//ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js"></script>
      <script src="//ajax.googleapis.com/ajax/libs/chrome-frame/1.0.3/CFInstall.min.js">
    </body>
    </html>"""
    doc = bs4.BeautifulSoup(content)
 
    doc_features =  list(features.scripts(doc))
    eq_(
      doc_features,
      [('script', u'//ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js'), 
      ('script', u'//ajax.googleapis.com/ajax/libs/chrome-frame/1.0.3/CFInstall.min.js')]
    )

  def test_links(self):
    doc = bs4.BeautifulSoup("""
    <html>
    <body>
      <a href="http://blah.com">blah</a>
    </body>
    </html>
    """)
    doc_features = list(features.links(doc))
    eq_(
      doc_features,
      [('links', u'http://blah.com')]
    )
    