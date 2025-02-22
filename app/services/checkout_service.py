from app.services.order_service import order_service
from app.services.cart_service import cart_service
from app.services.discount_service import discount_service
from fastapi import HTTPException

class CheckoutService:
    async def process_checkout(self, discount_code: str = None):
        """Processes the checkout flow, including discount validation."""
        # Fetch cart items
        cart_data = await cart_service.get_cart_items()
        cart_items = cart_data.get('cart', [])

        # Ensure cart is not empty
        if not cart_items:
            raise HTTPException(status_code=400, detail="Cart is empty")

        # Ensure every item has a price
        for item in cart_items:
            if "price" not in item:
                raise HTTPException(status_code=400, detail=f"Price missing for product {item['product_id']}")

        # Calculate total amount
        total_amount = sum(item["quantity"] * item["price"] for item in cart_items)
        discount_applied_amount = 0
        applied_discount_code = None
        
        # Validate discount code if provided
        if discount_code:
            is_valid = await discount_service.validate_discount_code(discount_code)
            if is_valid:
                discount_applied_amount = await discount_service.apply_discount(total_amount, discount_code)
                applied_discount_code = discount_code  # Store code
                total_amount -= discount_applied_amount
                await discount_service.mark_discount_as_used(discount_code)  # Mark as used
            else:
                raise HTTPException(status_code=400, detail="Invalid or expired discount code")

        # Place the order
        order_response = await order_service.place_order(cart_items, total_amount, discount_applied_amount, applied_discount_code)

        # Check if the order qualifies for a discount
        if await order_service.is_nth_order():
            new_discount_code = await discount_service.generate_discount_code()
            order_response['new_discount_code_generated'] = new_discount_code

        # Clear the cart after successful order placement
        await cart_service.clear_cart()

        return order_response

checkout_service = CheckoutService()
