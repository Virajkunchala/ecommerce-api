from fastapi import APIRouter, HTTPException, Depends
from app.services.cart_service import cart_service
from pydantic import BaseModel, ValidationError
from app.models.cart import CartItem

router = APIRouter()



@router.post("/items")
async def add_item_to_cart(item: CartItem):
    try:
        updated_cart = await cart_service.add_to_cart(item.product_id, item.quantity)
        return {"message": "Item added to cart", "cart": updated_cart}
    except ValidationError as ve:
        raise HTTPException(status_code=400, detail=f"Invalid data: {ve.errors()}")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/")
async def view_cart():
    return await cart_service.get_cart_items()

@router.post("/clear")
async def clear_cart():
    return await cart_service.clear_cart() 

