from fastapi import APIRouter, Depends, HTTPException
from app.services.order_service import order_service
from app.services.cart_service import cart_service
from app.services.discount_service import discount_service

router = APIRouter()

@router.post("/checkout")
async def checkout(discount_code: str = None):
    cart_data = await cart_service.get_cart_items()
    cart_items = cart_data.get('cart', [])

    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    # Ensure every item has a price
    for item in cart_items:
        if "price" not in item:
            raise HTTPException(status_code=400, detail=f"Price missing for product {item['product_id']}")

    # Calculate total amount
    total_amount=sum(item["quantity"]*item['price'] for item in cart_items)

    discount_percentage = 0
    discount_applied = 0

    # Validate Discount Code
    if discount_code:
        try:
            discount_percentage = await discount_service.validate_discount_code(discount_code)
            discount_applied = (discount_percentage / 100) * total_amount
            total_amount -= discount_applied
        except HTTPException as e:
            raise e  
        
        
    previous_order_count = order_service.order_count


    # Place the order
    order_response = await order_service.place_order(cart_items, total_amount, discount_applied)

    # Generate a new discount code 
    new_discount_code = None
    if (previous_order_count + 1) % discount_service.nth_order == 0:
        new_discount_code = await discount_service.generate_discount_code()

    # Clear the cart 
    await cart_service.clear_cart()

    # Attach new discount code 
    if new_discount_code:
        order_response["new_discount_code"] = new_discount_code

    return order_response