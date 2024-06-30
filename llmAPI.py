from fastapi import FastAPI, Path, Query, HTTPException, status
from pydantic import BaseModel
from llm import get_recipes
from fastapi.responses import JSONResponse
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
async def request_recipes(ingredients: Ingredients):
    recipes = get_recipes(ingredients_list=ingredients.ingredients_list, blacklisted_ingredients=ingredients.blacklisted_ingredients, 
    max_retries=3)

    if "error" in recipes.keys():
        return JSONResponse(status_code=404, content=recipes)
    
    return recipes


handler = Mangum(app)