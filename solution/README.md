# Elliott Perryman
## Solution Approach:
I did not understand there was a dynamic programming solution at first. It took me a bit to think about how I should think of the problem. I implemented a depth first search of the paths and used this to generate many more test cases. Then I implemented a dynamic programming solution that has time complexity O(T * P * B * |E|), where T is the time limit, P is the number of planets, B is the number of bounty hunters, and |E| is the number of edges. This solution is much faster. 

## Design Choices
 * I use python: I could rewrite it in C, but this would be a decent amount of time for not a huge payoff
 * I use sklearn to read the database into memory. If the database was so large that as to not fit in memory, I think the depth first search would be so slow anyways as to be bad for a server
 * I use fastAPI and uvicorn for running the frontend: these seemed very concise and accomplish the task
 * I use json schemas for validation. I could use a fastAPI style json validation, but I want to keep the documentation low, and adding this would mean that a change in the problem specs would require more changes in code. Right now, a change in the data format would necessitate the following:
    - changing the schemas.json file to align with specs
    - changing the class that uses the data
    - changing the part of the algorithm that uses the data
 * I use classes for the empire and millenium falcon data: I wanted to abstract away certain tasks from the algorithm

## How to run:
Clone the repo:
```bash
git clone https://github.com/elliottperryman/developer-test
```

make a local environment (I assume your python 3 is called python3)
```bash
cd solution
python3 -m venv env
source env/bin/activate
```

Update pip and install
```bash
pip install -U pip
pip install -r requirements.txt
pip install .
```

Now you can run the CLI like so (assuming your json file locations are right):
```bash
give-me-the-odds examples/example1/empire.json examples/example1/millennium-falcon.json
```

And the frontend runs with (assuming you are in developer-test/solution):
```bash
uvicorn frontend.main:app
```

## Things to do:
 * error logging

