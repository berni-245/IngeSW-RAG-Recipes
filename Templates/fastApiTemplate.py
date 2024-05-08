from fastapi import FastAPI, Path, Query, HTTPException, status
from typing import Optional # For Better read of code
from pydantic import BaseModel # To make a POST method I need to create a class that inherits from BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    brand: Optional[str] = None
    
class UpdateItem(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    brand: Optional[str] = None

""" @app.get("/") # root endpoint
def home():
    return {"Data": "Testing"}

@app.get("/about") # /about endpoint
def about():
    return {"Data": "About"}
 """
 
inventory = {
     1: {
         "name": "Milk",
         "price": 3.99,
         "brand": "Regular"
     }
 }

""" 
@app.get("/get-item/{item_id}/{name}")
def get_item(item_id: int, name: str):
    return inventory[item_id]
    # return inventory[item_id][name]
 """ 

@app.get("/get-item/{item_id}")
def get_item(item_id: int = Path(description="The ID of the item you would like to view", gt=0)):
    return inventory[item_id]

"""          
# For FastAPI it doesn't matter the order you pass the Query parameters, but for python it does matter when you pass required parameter AFTER optional parameters, you can escape with by adding the * at first, or reordering parameters
@app.get("/get-by-name")
def get_item(*, name: Optional[str] = None, test: str): 
    for item_id in inventory:
        if inventory[item_id]["name"] == name:
            return inventory[item_id]
    return {"Data": "Not found D:"}
# Examples

# http://127.0.0.1:8000/get-by-name?name=Milk&test=2 -> {"name":"Milk","price":3.99,"brand":"Regular"}
# http://127.0.0.1:8000/get-by-name?name=Berni -> {"detail":[{"type":"missing","loc":["query","test"],"msg":"Field required","input":null}]}
# http://127.0.0.1:8000/get-by-name?name=Berni&test=2 -> {"Data":"Not found D:"}
# http://127.0.0.1:8000/get-by-name?test=2&name=Milk -> {"name":"Milk","price":3.99,"brand":"Regular"} 
"""

@app.get("/get-by-name/{item_id}")
def get_item(*, item_id: int, name: Optional[str] = None, test: int): 
    for item_id in inventory:
        if inventory[item_id]["name"] == name:
            return inventory[item_id]
    # return {"Data": "Not found D:"}
    # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    raise HTTPException(status_code=404, detail="Item name not found")

# http://127.0.0.1:8000/get-by-name/1?test=2&name=Milk -> {"name":"Milk","price":3.99,"brand":"Regular"} 

# to test post, put or delete use http://127.0.0.1:8000/docs

@app.post("/create-item/{item_id}")
def create_item(item_id: int, item: Item):
    if item_id in inventory:
        raise HTTPException(status_code=400, detail="Item ID already exists")
    
    #inventory[item_id] = {"name": item.name, "brand": item.brand, "price": item.price}
    inventory[item_id] = item
    return inventory[item_id]

@app.put("/update-item/{item_id}")
def update_item(item_id: int, item: UpdateItem):
    if item_id not in inventory:
        raise HTTPException(status_code=404, detail="Item ID does not exist")
    
    if item.name != None:
        inventory[item_id]["name"] = item.name
        
    if item.price != None:
        inventory[item_id]["price"] = item.price
    
    if item.brand != None:
        inventory[item_id]["brand"] = item.brand
        
    return inventory[item_id] 

@app.delete("/delete-item")
def delete_item(item_id: int = Query(..., description="The ID of the item to delete", gt=0)):
    if item_id not in inventory:
        raise HTTPException(status_code=404, detail="Item ID does not exist")
        
    del inventory[item_id]
    return {"Success": "Item deleted!"}