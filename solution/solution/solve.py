import numpy as np
from solution.empire import Empire
from solution.falcon import MillenniumFalcon

DEBUG = False

def calc_prob(n)->int:
  """
    The expression given has a closed form. Chopping off the first term (0.1)
      gives a geometric series with a=0.09, r = 0.9, which can be solved in O(1)
    This solutiond implements the expression and rounds the percent type output
  """
  if n == 0: return 100
  if n == 1: return 90
  return round(100*(1- (0.1 + 0.09 * (1 - 0.9**(n-1)) / (1 - 0.9))))

if DEBUG:

  def solve(villains:Empire, heroes:MillenniumFalcon, verbose=False)->int:
    """
    This is a depth first search with the following states:
      time: cannot go longer than the deadline of the empire
      location: should be moving to the destination 
      encounters: how many encounters with bounty hunters have there been
      fuel_leval: what is the current fuel range of the falcon

      This has exponential time complexity
      """
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

  def _gen_problems(i):
    import os
    import json
    ex_dir = 'example'+str(i)
    # make directory and db file
    os.system('mkdir -p ../../examples/'+ex_dir)
    os.system('cp ../../examples/example1/universe.db ../../examples/'+ex_dir+'/universe.db')

    # make falcon data
    falcon = MillenniumFalcon('../../examples/example1/millennium-falcon.json')
    planets = np.unique(np.append(falcon.df['origin'].values, falcon.df['destination'].values))
    autonomy = np.random.randint(low=2, high=9)
    src, dest = np.random.choice(planets, size=2, replace=False)
    with open('../../examples/'+ex_dir+'/millennium-falcon.json', 'w') as file:
      json.dump({
        'autonomy': autonomy,
        'departure': src,
        'arrival': dest,
        'routes_db': 'universe.db'
      }, file, indent=2)
    
    # make empire data
    countdown = max(autonomy, np.random.randint(low=1, high=15))
    bh = [{'planet':p, 'day':day} for p in planets for day in range(1,countdown)]
    bh = [x for x in bh if np.random.random()<0.8]
    with open('../../examples/'+ex_dir+'/empire.json', 'w') as file:
      json.dump({
        'countdown': countdown,
        'bounty_hunters': bh
      }, file, indent=2)
    
    with open('../../examples/'+ex_dir+'/answer.json', 'w') as file:
      soln = solve(
        Empire('../../examples/'+ex_dir+'/empire.json'), 
        MillenniumFalcon('../../examples/'+ex_dir+'/millennium-falcon.json')
      )
      json.dump({
        'odds': soln/100
      }, file, indent=2)

  def gen_problems():
    for i in range(5,100):
      _gen_problems(i)

else:
  def solve(villains:Empire, heroes:MillenniumFalcon)->int:
    """
      This is a dynamic programming solution. We have a big table
       (I know I can be more efficient with memory here), where
       each row is a time, place, and # of bounty hunter encounters.
       Every element of the table is an amount of fuel in the Falcon.
       At every time we want to take the more fuel efficient way, everythign
       else being equal. So, we iterate through the possibilities and progress 
       through the tables. At the end, we have a table for each number of encounters
       with the bounty hunters. We pick the first time at the destination with the 
       lowest number of encounters with the bounty hunters.
    """
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
          if i+1<=time_limit:
            dynamic_prog_table[i+1, j, k+int(villains.check_bounty_hunters(i+1, planet))] = fuel_max
          # for every reachable place
          for dest, travel_time in heroes.find_neighbors(planet, fuel_level):
            if i + travel_time <= time_limit:  
              # update the table with the most fuel efficient way to get to this location
              dynamic_prog_table[i+travel_time, planet_mapping[dest], k+int(villains.check_bounty_hunters(i+travel_time, dest))] = max(
                dynamic_prog_table[i+travel_time, planet_mapping[dest], k+int(villains.check_bounty_hunters(i+travel_time, dest))],
                fuel_level - travel_time
              )
    if all(dynamic_prog_table[-1,planet_mapping[end], :]<0): return 0
    min_val = np.where(dynamic_prog_table[:, planet_mapping[end], :]>=0)[1].min()
    return calc_prob(min_val)
