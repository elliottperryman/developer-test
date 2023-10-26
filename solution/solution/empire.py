from jsonschema import validate
from solution.schemas import empire_schema
import json

class Empire:
  def __init__(self, filePath:str, data=None):
    if data is None:
      try:
        with open(filePath, 'r') as file:
          data = json.load(file)
      except FileNotFoundError as e:
        print('did not find empire file - e')
        raise e
      except json.JSONDecodeError as e:
        print('json error')
        raise e
    validate(instance=data, schema=empire_schema)
    self.time_limit = data['countdown']

    self.bounty_hunter_map = {}
    for x in data['bounty_hunters']:
      if x['planet'] not in self.bounty_hunter_map:
        self.bounty_hunter_map[x['planet']] = set()
      self.bounty_hunter_map[x['planet']].add(x['day'])

  def check_bounty_hunters(self, time, loc):
    if loc in self.bounty_hunter_map:
      if time in self.bounty_hunter_map[loc]:
        return True
    return False