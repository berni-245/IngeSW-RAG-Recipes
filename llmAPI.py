from fastapi import FastAPI, Path, Query, HTTPException, status
from pydantic import BaseModel
from llm import get_recipes
from mangum import Mangum

class Ingredients(BaseModel):
    Ingredients_list: list

app = FastAPI()

@app.post("/request-recipes")
def request_recipes(ingredients: Ingredients):
    return get_recipes(ingredients)

handler = Mangum(app)