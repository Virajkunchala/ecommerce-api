from fastapi import APIRouter, HTTPException
from app.services.checkout_service import checkout_service
from app.services.order_service import order_service


router = APIRouter()

@router.post("/checkout")
async def checkout(discount_code: str = None):
    """Order Checkout API"""
    try:
        order_response = await checkout_service.process_checkout(discount_code)
        return order_response
    except HTTPException as e:
        raise e
    
@router.get("/orders")
async def get_orders():
    """API to retrieve order history"""
    return await order_service.get_orders()
