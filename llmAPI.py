from fastapi import FastAPI, Path, Query, HTTPException, status
from pydantic import BaseModel
from llm import get_recipes
from mangum import Mangum

class Ingredients(BaseModel):
    ingredients_list: list
    blacklisted_ingredients: list

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "ingredients_list": ["carne", "tomate", "lechuga"],
                    "blacklisted_ingredients": ["carne"],
                }
            ]
        }
    }


app = FastAPI()

@app.post("/request-recipes")
def request_recipes(ingredients: Ingredients):
    return get_recipes(ingredients_list=ingredients.ingredients_list, blacklisted_ingredients=ingredients.blacklisted_ingredients)

handler = Mangum(app)