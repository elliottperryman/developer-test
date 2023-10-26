import numpy as np
from solution.empire import Empire
from solution.falcon import MillenniumFalcon

def calc_prob(n):
  if n == 0: return 100
  return round(100*(1 - (0.1 + sum((0.9)**k/10 for k in range(1,n)))))

def solve(villains:Empire, heroes:MillenniumFalcon, verbose=False):
  solns = []
  best_val = [-1]

  def recurse(time, location, encounters, fuel_level, trace):
    if verbose:
      trace = trace + [(location, time)]
    if time > villains.time_limit:
      return
    if villains.check_bounty_hunters(time, location):
      encounters += 1
    if location == heroes.destination:
      if verbose:
        solns.append((trace, encounters))
      if calc_prob(encounters)>best_val[0]:
        best_val[0] = calc_prob(encounters)
      return
    recurse(time+1, location, encounters, heroes.max_fuel_range, trace)
    for planet, travel_time in heroes.find_neighbors(location, fuel_level):
      recurse(time+travel_time, planet, encounters, fuel_level-travel_time, trace)

  recurse(0, heroes.start, 0, heroes.max_fuel_range, [])

  if verbose:
    print('all solutions:', *solns, sep='\n')
  if best_val[0] == -1:
    if verbose: 
      print('no path fast enough')
    return 0
  elif best_val[0] == 0:
    if verbose:
      print('caught by bounty hunters on any path')
    return 0
  else:
    return best_val[0]