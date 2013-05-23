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
      insight = json.load(open(insight_path))
      insight['id'] = os.path.basename(insight_path)
      yield insight
    except:
      app.logger.exception("Error parsing %s", insight_path)
