## Things to do:

 * ask about rounding percents
 * mistake in the readme?
 * error logging
 * commenting
 * fix setup.py with details
 * write frontend
 * write readme
 * form for json


python3 -m venv env
source env/bin/activate
pip install -U pip
pip install -r requirements.txt
pip install .
run frontend
uvicorn frontend.main:app --reload