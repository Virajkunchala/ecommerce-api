from fastapi import APIRouter, Depends, HTTPException
from app.services.order_service import order_service
from app.services.cart_service import cart_service
from app.services.discount_service import discount_service

router = APIRouter()

@router.post("/checkout")
async def checkout(discount_code:str=None):
    cart_items=await cart_service.get_cart_items()
    
    if not cart_items:
        raise HTTPException(status_code=400,detail="cart is empty")
    
    total_amount=sum(item["quantity"]*10 for item in cart_items)
    discount_percentage =0
    discount_applied=total_amount*discount_percentage
    total_amount -=discount_applied
    
    order_response=await order_service.place_order(cart_items,total_amount,discount_applied)
    
    new_discount_code=0
    
    await cart_service.clear_cart()
    
    if new_discount_code:
        order_response['new_discount_code']=new_discount_code
        
        
    return order_response


