import pytest
from fastapi.exceptions import HTTPException
from app.services.cart_service import CartService


@pytest.mark.asyncio
async def test_add_to_cart():
    cart_service = CartService() 

    #adding items to cart
    cart=await cart_service.add_to_cart(1,1)
    
    assert len(cart)==1
    assert cart["cart"][0]['product_id'] == 1
    assert cart["cart"][0]["quantity"] == 1
    
    # Add same item again (should increase quantity)
    cart=await cart_service.add_to_cart(1,2)
    assert cart["cart"][0]['quantity'] == 3
  
@pytest.mark.asyncio
async def test_add_invalid_quantity():
    cart_service = CartService() 
    
    with pytest.raises(HTTPException) as exc:
        await cart_service.add_to_cart(1,0)
       
    assert exc.value.status_code == 400
    assert "Quantity must be greater than 0" in str(exc.value.detail)
    
@pytest.mark.asyncio
async def test_get_cart_items():
    cart_service = CartService() 
    # Add items
    await cart_service.add_to_cart(1, 1)
    cart = await cart_service.get_cart_items()
    
    assert len(cart) == 1
    assert cart["cart"][0]['product_id'] == 1
    assert cart["cart"][0]["quantity"] == 1
        
@pytest.mark.asyncio
async def test_clear_cart():
    cart_service = CartService() 
        
    await cart_service.add_to_cart(1, 2)
    await cart_service.clear_cart()
    
    cart_response  = await cart_service.get_cart_items()
    cart = cart_response['cart']
    assert len(cart) == 0
    
    
