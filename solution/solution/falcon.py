import json, sqlite3, os
from jsonschema import validate
import pandas as pd
import numpy as np
from solution.schemas import falcon_schema

class MillenniumFalcon:
  def __init__(self, filePath:str):
    try:
      with open(filePath, 'r') as file:
        data = json.load(file)
    except FileNotFoundError as e:
       print('did not find empire file')
       raise e
    except json.JSONDecodeError as e:
      print('json error')
      raise e

    validate(instance=data, schema=falcon_schema)
    self.max_fuel_range = data['autonomy']
    self.start = data['departure']
    self.destination = data['arrival']
    self.db_file = os.path.dirname(filePath)+'/'+data['routes_db']
    if not os.path.isfile(self.db_file):
      raise RuntimeError('database file not found at {}'.format(self.db_file))
    self.db_setup()
  def db_setup(self):
    conn = sqlite3.connect(self.db_file)
    self.df = pd.read_sql_query("SELECT * from ROUTES", conn)
  def find_neighbors(self, loc, fuel_range):
    return np.vstack((
        self.df[np.logical_and(self.df['origin']==loc, self.df['travel_time']<=fuel_range)][['destination', 'travel_time']].values,
        self.df[np.logical_and(self.df['destination']==loc, self.df['travel_time']<=fuel_range)][['origin', 'travel_time']].values
    ))