import numpy as np
# from solution.empire import Empire
# from solution.falcon import MillenniumFalcon
from empire import Empire
from falcon import MillenniumFalcon

def calc_prob(n):
  if n == 0: return 100
  if n == 1: return 90
  return round(100*(1- (0.1 + 0.09 * (1 - 0.9**(n-1)) / (1 - 0.9))))

def solve(villains:Empire, heroes:MillenniumFalcon):
  fuel_max = heroes.max_fuel_range
  start = heroes.start
  end = heroes.destination
  time_limit = villains.time_limit
  df = heroes.df
  bounty_hunter_map = villains.bounty_hunter_map
  planets = np.unique(np.append(df['origin'].values, df['destination'].values))
  planet_mapping = {p:i for i,p in enumerate(planets)}
  num_bounty_hunters = sum([len(bounty_hunter_map[planet]) for planet in bounty_hunter_map])

  dynamic_prog_table = -1*np.ones((time_limit+1, len(planets), num_bounty_hunters+1), dtype=int)
  dynamic_prog_table[0, planet_mapping[start], int(villains.check_bounty_hunters(0, start))] = fuel_max

  # print(dynamic_prog_table.shape)
  
  for i in range(time_limit+1):
    for j,planet in enumerate(planets):
      for k in range(num_bounty_hunters):
        # if location is unreachable
        if dynamic_prog_table[i,j,k] < 0: 
          continue
        # if at destination
        if planet == end:
          continue
        # look at current fuel
        fuel_level = dynamic_prog_table[i,j,k]
        # refueling option
        if i+1<time_limit:
          dynamic_prog_table[i+1, j, k+int(villains.check_bounty_hunters(i+1, planet))] = fuel_max
        # all neighbors
        for dest, travel_time in heroes.find_neighbors(planet, fuel_level):
          if i + travel_time <= time_limit:  
            # print(i+travel_time, dest, k+int(villains.check_bounty_hunters(i+travel_time, dest)))
            dynamic_prog_table[i+travel_time, planet_mapping[dest], k+int(villains.check_bounty_hunters(i+travel_time, dest))] = max(
              dynamic_prog_table[i+travel_time, planet_mapping[dest], k+int(villains.check_bounty_hunters(i+travel_time, dest))],
              fuel_level - travel_time
            )
  # for enc in range(num_bounty_hunters):
  #   print(f'{enc} encounters')
  #   print(dynamic_prog_table[:,:,enc])
  # print('dest')
  # print(dynamic_prog_table[:, planet_mapping[end], :])
  # print('hi')
  if all(dynamic_prog_table[-1,planet_mapping[end], :]<0): return 0
  min_val = np.where(dynamic_prog_table[-1,planet_mapping[end], :]>=0)[0].min()
  return calc_prob(min_val)

# def solve(villains:Empire, heroes:MillenniumFalcon, verbose=False):
#   """
#   This is a depth first search with the following states:
#     time: cannot go longer than the deadline of the empire
#     location: should be moving to the destination 
#     encounters: how many encounters with bounty hunters have there been
#     fuel_leval: what is the current fuel range of the falcon
#     """
#   solns = []
#   best_val = [-1]

#   def recurse(time, location, encounters, fuel_level, trace):
#     if verbose:
#       trace = trace + [(location, time)]
#     if time > villains.time_limit:
#       return
#     if villains.check_bounty_hunters(time, location):
#       encounters += 1
#     if location == heroes.destination:
#       if verbose:
#         solns.append((trace, encounters))
#       if calc_prob(encounters)>best_val[0]:
#         best_val[0] = calc_prob(encounters)
#       return
#     recurse(time+1, location, encounters, heroes.max_fuel_range, trace)
#     for planet, travel_time in heroes.find_neighbors(location, fuel_level):
#       recurse(time+travel_time, planet, encounters, fuel_level-travel_time, trace)

#   recurse(0, heroes.start, 0, heroes.max_fuel_range, [])

#   if verbose:
#     print('all solutions:', *solns, sep='\n')
#   if best_val[0] == -1:
#     if verbose: 
#       print('no path fast enough')
#     return 0
#   elif best_val[0] == 0:
#     if verbose:
#       print('caught by bounty hunters on any path')
#     return 0
#   else:
#     return best_val[0]