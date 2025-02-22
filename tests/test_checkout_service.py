import pytest
from fastapi import HTTPException
from unittest.mock import AsyncMock
from app.services.checkout_service import CheckoutService
from app.services.cart_service import cart_service
from app.services.order_service import order_service
from app.services.discount_service import discount_service

@pytest.fixture
def checkout_service():
    return CheckoutService()

@pytest.mark.asyncio
async def test_process_checkout_empty_cart(checkout_service):
    cart_service.get_cart_items = AsyncMock(return_value={'cart': []})
    
    with pytest.raises(HTTPException) as exc_info:
        await checkout_service.process_checkout()
    
    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Cart is empty"

@pytest.mark.asyncio
async def test_process_checkout_item_missing_price(checkout_service):
    cart_service.get_cart_items = AsyncMock(return_value={'cart': [{'product_id': '1', 'quantity': 1}]})
    
    with pytest.raises(HTTPException) as exc_info:
        await checkout_service.process_checkout()
    
    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Price missing for product 1"

@pytest.mark.asyncio
async def test_process_checkout_no_discount(checkout_service):
    mock_cart_items = [{'product_id': '1', 'quantity': 1, 'price': 50.0}]
    cart_service.get_cart_items = AsyncMock(return_value={'cart': mock_cart_items})
    order_service.place_order = AsyncMock(return_value={
        'message': 'Order placed successfully', 'order_id': 1, 'total_amount': 50.0, 'discount_applied': 0
    })
    cart_service.clear_cart = AsyncMock()
    order_service.is_nth_order = AsyncMock(return_value=False)
    discount_service.generate_discount_code = AsyncMock(return_value=None)
    
    order_response = await checkout_service.process_checkout()
    
    assert order_response["message"] == "Order placed successfully"
    assert order_response["total_amount"] == 50.0
    assert order_response["discount_applied"] == 0
    order_service.place_order.assert_called_once_with(mock_cart_items, 50.0, 0, None)
    cart_service.clear_cart.assert_called_once()
    discount_service.generate_discount_code.assert_not_called()

@pytest.mark.asyncio
async def test_process_checkout_with_valid_discount(checkout_service):
    mock_cart_items = [{'product_id': '1', 'quantity': 1, 'price': 100.0}]
    cart_service.get_cart_items = AsyncMock(return_value={'cart': mock_cart_items})
    discount_service.validate_discount_code = AsyncMock(return_value=True)
    discount_service.apply_discount = AsyncMock(return_value=10.0)
    discount_service.mark_discount_as_used = AsyncMock()
    order_service.place_order = AsyncMock(return_value={
        'message': 'Order placed successfully', 'order_id': 1, 'total_amount': 90.0, 'discount_applied': 10.0, 'discount_code': 'VALID_CODE'
    })
    cart_service.clear_cart = AsyncMock()
    order_service.is_nth_order = AsyncMock(return_value=False)
    discount_service.generate_discount_code = AsyncMock(return_value=None)
    
    order_response = await checkout_service.process_checkout(discount_code="VALID_CODE")
    
    assert order_response["message"] == "Order placed successfully"
    assert order_response["total_amount"] == 90.0
    assert order_response["discount_applied"] == 10.0
    assert order_response["discount_code"] == "VALID_CODE"
    discount_service.validate_discount_code.assert_called_once_with("VALID_CODE")
    discount_service.apply_discount.assert_called_once_with(100.0, "VALID_CODE")
    discount_service.mark_discount_as_used.assert_called_once_with("VALID_CODE")
    cart_service.clear_cart.assert_called_once()
    discount_service.generate_discount_code.assert_not_called()

@pytest.mark.asyncio
async def test_process_checkout_generates_new_discount_on_nth_order(checkout_service):
    mock_cart_items = [{'product_id': '1', 'quantity': 1, 'price': 50.0}]
    cart_service.get_cart_items = AsyncMock(return_value={'cart': mock_cart_items})
    order_service.place_order = AsyncMock(return_value={
        'message': 'Order placed successfully', 'order_id': 3, 'total_amount': 50.0, 'discount_applied': 0
    })
    cart_service.clear_cart = AsyncMock()
    order_service.is_nth_order = AsyncMock(return_value=True)
    discount_service.generate_discount_code = AsyncMock(return_value="NEW_DISCOUNT_CODE")
    
    order_response = await checkout_service.process_checkout()
    
    assert order_response["message"] == "Order placed successfully"
    assert order_response["new_discount_code_generated"] == "NEW_DISCOUNT_CODE"
    order_service.place_order.assert_called_once()
    discount_service.generate_discount_code.assert_called_once()
    cart_service.clear_cart.assert_called_once()
