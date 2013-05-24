import os
import json
from .app import app

def list_path(path):
  assert not os.path.isabs(path)
  abs_path = os.path.join(app.root_path, path)

  return [
    os.path.join(abs_path, f)
    for f in os.listdir(abs_path)
  ]



def all():

  for insight_path in list_path("insights"):
    try:

      insight = dict(
        id = os.path.splitext(os.path.basename(insight_path))[0],
        content=open(insight_path).read(),
        limit = 10,
        columns = ""
      )
      yield insight
    except GeneratorExit:
      raise
    except:
      app.logger.exception("Error parsing %s", insight_path)

def get(id):

  for insight in all():
    if insight['id'] == id:
      return insight