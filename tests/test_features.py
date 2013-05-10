from nose.tools import eq_
import bs4

from . import TestCase

import features

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

    doc_features =  list(features.script(doc(content)))
    eq_(
      doc_features,
      [('script', u'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js'), 
      ('script', u'http://ajax.googleapis.com/ajax/libs/chrome-frame/1.0.3/CFInstall.min.js')]
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
        ('link_to', 'blah.com'),
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
    doc_features = list(features.tag(doc(content)))
    self.assertSequenceEqual(
      doc_features,
      [
        ('tag', 'html'),
        ('tag', 'html>body'),
        ('tag', 'html>body>a'),
        ('tag', 'html>body>a'),
        ('tag', 'html>body>div'),
        ('tag', 'html>body>div>span'),
        ('tag', 'html>body>div>div'),
        ('tag', 'html>body>div>div>ul'),
        ('tag', 'html>body>div>div>ul>li'),
        ('tag', 'html>body>div>div>ul>li')
      ]
    )
   