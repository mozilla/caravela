import unittest
import boto
import os
import bs4

class TestCase(unittest.TestCase):
  def setUp(self):
    # download a sample file
    self.doc = bs4.BeautifulSoup(open(self.docs()[0]))

  def docs(self):
    dirname = os.path.dirname(__file__)
    doc_path = os.path.join(dirname, 'fixtures', 'html')
    return [ os.path.join(doc_path, doc) for doc in os.listdir(doc_path)]