from jsonschema import validate
from solution.schemas import empire_schema
import json

class Empire:
  """
  This class holds all the data for the empire.
  Notes:
    I read in the data either by json file or a data string
    I convert the list of bounty hunters to a O(1) lookup data structure
    I have a simple tool for looking up if bounty hunters are present
  """
  def __init__(self, filePath:str, data=None):
    # load file if data string is not given
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
    # need to validate json data
    validate(instance=data, schema=empire_schema)
    # save json data
    self.time_limit = data['countdown']
    # list lookup is O(N), we want to use sets & dicts for O(1)
    self.bounty_hunter_map = {}
    for x in data['bounty_hunters']:
      if x['planet'] not in self.bounty_hunter_map:
        self.bounty_hunter_map[x['planet']] = set()
      self.bounty_hunter_map[x['planet']].add(x['day'])
  # simple dict of sets lookup
  def check_bounty_hunters(self, time, loc):
    if loc in self.bounty_hunter_map:
      if time in self.bounty_hunter_map[loc]:
        return True
    return False