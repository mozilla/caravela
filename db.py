from os.path import dirname, join
import sys

from splicer import DataSet, Relation
from splicer.servers.file_server import FileServer

import splicer_console
from splicer_discodb import DiscoDBServer


def init(**tables):
  """
    Returns a dataset to work with the discodb specified by path
  """

  dataset = DataSet()
  dataset.add_server(DiscoDBServer(**tables))
  dataset.add_server(FileServer(
    top_sites=dict(
      root_dir=join(dirname(__file__), 'data'),
      pattern="alexa-top1m-{date}.csv",
      decode="auto"
    )
  ))

  dataset.select(
    'date, column_0 as rank, column_1 as site'
  ).frm('top_sites').limit(10).create_view('top_10')


  return dataset


if __name__ == "__main__":
  dataset = init(docs=sys.argv[1])
  splicer_console.init(dataset)