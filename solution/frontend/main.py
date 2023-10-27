from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from jsonschema import validate
from solution.schemas import empire_schema
from solution.solve import solve
from solution.falcon import MillenniumFalcon
from solution.empire import Empire
from typing import Dict

app = FastAPI()
templates = Jinja2Templates(directory="frontend")

@app.get("/")
async def root(request:Request):
    print(request)
    return templates.TemplateResponse('page.html', context={'request':request})

@app.post("/")
async def create_item(data:Dict):
    print(data)
    validate(data, schema=empire_schema)
    odds = solve(Empire(filePath=None, data=data), MillenniumFalcon('data/millennium-falcon.json'))
    return {'odds':odds}