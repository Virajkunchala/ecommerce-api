import pytest
from fastapi.exceptions import HTTPException
from app.services.cart_service import CartService


@pytest.mark.asyncio
async def test_add_to_cart():
    cart_service = CartService()

    # Adding an item to the cart
    cart = await cart_service.add_to_cart(1, 1)
    
    assert len(cart["cart"]) == 1
    assert cart["cart"][0]['product_id'] == 1
    assert cart["cart"][0]["quantity"] == 1
    
    # Add the same item again (should increase quantity)
    cart = await cart_service.add_to_cart(1, 2)
    assert cart["cart"][0]['quantity'] == 3
    assert cart["cart"][0]["total_price"] == 300  # Total price should reflect 3 * 100


@pytest.mark.asyncio
async def test_add_invalid_quantity():
    cart_service = CartService()
    
    with pytest.raises(HTTPException) as exc:
        await cart_service.add_to_cart(1, 0)
    
    assert exc.value.status_code == 400
    assert "Quantity must be greater than 0" in str(exc.value.detail)
    

@pytest.mark.asyncio
async def test_add_invalid_product():
    cart_service = CartService()
    
    with pytest.raises(HTTPException) as exc:
        await cart_service.add_to_cart(999, 1)  # Invalid product ID
    
    assert exc.value.status_code == 400
    assert "Invalid product ID" in str(exc.value.detail)


@pytest.mark.asyncio
async def test_get_cart_items():
    cart_service = CartService()
    # Add items
    await cart_service.add_to_cart(1, 1)
    cart = await cart_service.get_cart_items()
    
    assert len(cart["cart"]) == 1
    assert cart["cart"][0]['product_id'] == 1
    assert cart["cart"][0]["quantity"] == 1


@pytest.mark.asyncio
async def test_clear_cart():
    cart_service = CartService()
    
    # Adding an item to the cart
    await cart_service.add_to_cart(1, 2)
    
    # Clearing the cart
    await cart_service.clear_cart()
    
    # Verifying cart is cleared
    cart_response = await cart_service.get_cart_items()
    cart = cart_response["cart"]
    assert len(cart) == 0
    assert cart_response["cart"] == []  # Ensure the cart is empty after clearing
