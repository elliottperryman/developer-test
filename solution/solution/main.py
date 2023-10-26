#!env/bin/python
import sys
from solution.solve import solve
from solution.empire import Empire
from solution.falcon import MillenniumFalcon

def main():
    if len(sys.argv)!=3:
        print('Usage: python main.py empire.json falcon.json', file=sys.stderr)
    else:
        print(solve(Empire(sys.argv[1]), MillenniumFalcon(sys.argv[2])))

if __name__=='__main__':
    main()
