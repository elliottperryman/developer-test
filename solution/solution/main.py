#!env/bin/python
import sys
# from solution.solve import solve
# from solution.empire import Empire
# from solution.falcon import MillenniumFalcon

from solve import solve
from empire import Empire
from falcon import MillenniumFalcon

def main():
    """
    just run the solve function and check for command line correctness
    """
    if len(sys.argv)!=3:
        print('Usage: python main.py empire.json falcon.json', file=sys.stderr)
    else:
        print(solve(Empire(sys.argv[1]), MillenniumFalcon(sys.argv[2])))

if __name__=='__main__':
    sys.argv = ['', '../../examples/example4/empire.json', '../../examples/example4/millennium-falcon.json']
    main()
