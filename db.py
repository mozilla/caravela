from os.path import dirname, join
import sys

from splicer import DataSet, Relation
from splicer.servers.file_server import FileServer

import splicer_console
import splicer_arc
from splicer_discodb import DiscoDBServer


def init(**tables):
  """
    Returns a dataset to work with the discodb specified by path
  """

  dataset = DataSet()
  dataset.add_server(DiscoDBServer(**tables))

  dataset.add_server(FileServer(
    common_crawl=dict(
      root_dir=join(dirname(__file__), 'data'),
      pattern="sample.arc.gz",
      decode="application/x-arc",
      #description="Raw documents from http://commoncrawl.org"
    )
  ))


  dataset.add_server(FileServer(
    top_sites=dict(
      #description="Top Sites as reported by Alexa",
      root_dir=join(dirname(__file__), 'data'),
      pattern="alexa-top1m-{date}.csv",
      decode="auto",
      schema=dict(
        fields=[
          dict(name="date", type="DATE"),
          dict(name="rank", type="STRING"),
          dict(name="site", type="STRING")
        ]
      )
    )
  ))

  dataset.frm('top_sites').limit(10).create_view('top_10')

  dataset.create_view(
    'outbound_links',
    "select link_to, count() "
    "from flatten(docs, 'link_to') "
    "group by link_to order by count desc"
  )

  dataset.create_view(
    'scripts',
    "select scripts as script, count() "
    "from flatten(docs, 'scripts') "
    "group by script order by count desc"
  )

  dataset.create_view(
    'servers',
    "select headers_value as server_name, count() " 
    "from flatten(docs, 'headers') " 
    "where headers_name = 'Server' "
    "group by server_name order by count desc"
  )

  return dataset


if __name__ == "__main__":
  dataset = init(docs=sys.argv[1])
  splicer_console.init(dataset)