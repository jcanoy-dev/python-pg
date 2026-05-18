from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, List, Optional

app = FastAPI()

# 1. Temporary in-memory database
db: List[Dict[str, float | int | str]] = [
    {"id": 1, "name": "Laptop", "price": 999.99},
    {"id": 2, "name": "Mouse", "price": 24.99}
]

# 2. Pydantic schema to validate data incoming via POST
class Item(BaseModel):
    name: str
    price: float

# 3. GET endpoint to fetch all items
@app.get("/items")
def get_items() -> Dict[str, List[Dict[str, float | int | str]]]:
    return {"items": db}

# 4. POST endpoint to add a new item
@app.post("/items")
def create_item(item: Item) -> Dict[str, Dict[str, float | int | str]]:
    new_item = {"id": len(db) + 1, "name": item.name, "price": item.price}
    db.append(new_item)
    return {"message": "Item added!", "item": new_item}


@app.get("/items/{item_id}")
def get_item_by_id(item_id: int):
    # Search the list for the matching ID
    for item in db:
        if item["id"] == item_id:
            return item
    
    # ❌ 4. Error Handling: If not found, return a 404 error
    raise HTTPException(status_code=404, detail="Item not found")

#  /items/search/?max_price=25
@app.get("/items/search/")
def search_items(max_price: Optional[float] = None):
    if max_price:
        # Filter items cheaper than or equal to max_price
        filtered_items = [item for item in db if item["price"] <= max_price]
        return {"filtered": filtered_items}
    
    return {"items": db}


# Update an existing item's price or name
@app.put("/items/{item_id}")
def update_item(item_id: int, updated_data: Item):
    for item in db:
        if item["id"] == item_id:
            item["name"] = updated_data.name
            item["price"] = updated_data.price
            return {"message": "Item updated successfully", "item": item}
    raise HTTPException(status_code=404, detail="Item skipped, not found")

# Delete an item from the temporary list
@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    for index, item in enumerate(db):
        if item["id"] == item_id:
            deleted_item = db.pop(index)
            return {"message": f"Deleted {deleted_item['name']}"}
    raise HTTPException(status_code=404, detail="Item not found")
