from fastapi import APIRouter, HTTPException
from app.services.admin_service import admin_service
from app.services.discount_service import discount_service

router = APIRouter()


@router.post("/discount_code")
async def create_discount_code(nth_order:int):
    """Endpoint to generate a discount code for every nth order.."""
   # Generate the discount code using the service
    discount_code = discount_service.generate_discount_code(nth_order)
    if not discount_code:
        raise HTTPException(status_code=400, detail="Failed to generate discount code.")
    return {"discount_code": discount_code}

@router.get("/orders")
async def get_order_stats():
    """Returns total orders, purchase amount, and discount amount."""
    return await admin_service.get_order_stats()

@router.get("/discounts")
async def get_available_discounts():
    """Returns all available (unused) discount codes."""
    return await admin_service.get_discount_codes()
