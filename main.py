from fastapi import FastAPI, APIRouter, HTTPException, Query
from typing import Optional, List
from pydantic import BaseModel
import uvicorn

app = FastAPI(title="Drugboard Drawing Tool", version="1.0.0")

router = APIRouter()

# Sample in-memory database
items = {}

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float

@router.get("/")
async def welcome_greeting():
    return "message: Welcome to Drugboard Drawing Tool"

@router.post("/items/", response_model=Item)
async def create_item(item: Item):
    if item.name in items:
        raise HTTPException(status_code=400, detail="Item already exists")
    items[item.name] = item
    return item


@router.get("/items/", response_model=List[Item])
async def read_items(skip: int = 0, limit: int = 10):
    return list(items.values())[skip : skip + limit]

@router.get("/items/{item_name}", response_model=Item)
async def read_item(item_name: str):
    if item_name not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return items[item_name]

@router.put("/items/{item_name}", response_model=Item)
async def update_item(item_name: str, item: Item):
    if item_name not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    items[item_name] = item
    return item

@router.delete("/items/{item_name}")
async def delete_item(item_name: str):
    if item_name not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    del items[item_name]
    return {"message": "Item deleted"}

@router.get("/search/")
async def search_items(q: str = Query(..., min_length=3, max_length=50)):
    results = [item for item in items.values() if q.lower() in item.name.lower()]
    return results

app.include_router(router, prefix="/api/v1")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)