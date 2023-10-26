from fastapi import FastAPI
from jsonschema import validate
from solution.schemas import empire_schema
from solution.solve import solve
from solution.falcon import MillenniumFalcon
from solution.empire import Empire
from typing import Dict

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/solve/")
async def create_item(data:Dict):
    print(data)
    validate(data, schema=empire_schema)
    odds = solve(Empire(filePath=None, data=data), MillenniumFalcon('data/millennium-falcon.json'))
    return {'odds':odds}