import json, sqlite3, os
from jsonschema import validate
import pandas as pd
import numpy as np
# from solution.schemas import falcon_schema
from schemas import falcon_schema

class MillenniumFalcon:
  """
  This class should have all the data for the heroes
  Notes:
    The json/data parts are the same as for Empire
    the database is read all at once
    Finding the neighbors is implemented as a method
  """
  def __init__(self, filePath:str):
    # read data
    try:
      with open(filePath, 'r') as file:
        data = json.load(file)
    except FileNotFoundError as e:
       print('did not find empire file')
       raise e
    except json.JSONDecodeError as e:
      print('json error')
      raise e
    # validate data
    validate(instance=data, schema=falcon_schema)
    # save data
    self.max_fuel_range = data['autonomy']
    self.start = data['departure']
    self.destination = data['arrival']
    self.db_file = os.path.dirname(filePath)+'/'+data['routes_db']
    # check for database file
    if not os.path.isfile(self.db_file):
      raise RuntimeError('database file not found at {}'.format(self.db_file))
    # put database in memory
    self.db_setup()
  def db_setup(self):
    conn = sqlite3.connect(self.db_file)
    self.df = pd.read_sql_query("SELECT * from ROUTES", conn)
  # a neighbor is within fuel range and has a destination or origin at loc
  def find_neighbors(self, loc, fuel_range):
    return np.vstack((
        self.df[np.logical_and(self.df['origin']==loc, self.df['travel_time']<=fuel_range)][['destination', 'travel_time']].values,
        self.df[np.logical_and(self.df['destination']==loc, self.df['travel_time']<=fuel_range)][['origin', 'travel_time']].values
    ))