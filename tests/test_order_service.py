import pytest
from app.services.order_service import OrderService

@pytest.fixture
def order_service():
    return OrderService(nth_order_threshold=3)

@pytest.mark.asyncio
async def test_place_order(order_service):
    initial_order_count = order_service.order_count
    cart_items = [{"product_id": "1", "quantity": 2, "price": 20.0}]
    total_amount = 40.0
    discount_applied = 0.0
    discount_code = None
    order_response = await order_service.place_order(cart_items, total_amount, discount_applied, discount_code)

    assert order_response["message"] == "Order placed successfully"
    assert order_response["order_id"] == initial_order_count + 1
    assert order_response["total_amount"] == total_amount
    assert order_response["discount_applied"] == discount_applied
    assert order_service.order_count == initial_order_count + 1
    assert len(order_service.orders) == 1
    placed_order = order_service.orders[0]
    assert placed_order["order_id"] == initial_order_count + 1
    assert placed_order["items"] == cart_items
    assert placed_order["total_amount"] == total_amount
    assert placed_order["discount_applied"] == discount_applied
    assert placed_order["discount_code"] is None


@pytest.mark.asyncio
async def test_is_nth_order(order_service):
    # Reset order count for  testing
    order_service.order_count = 0

    order_service.order_count = 1
    assert await order_service.is_nth_order() is False
    order_service.order_count = 2
    assert await order_service.is_nth_order() is False

    # Third order should be nth order
    order_service.order_count = 3
    assert await order_service.is_nth_order() is True
    order_service.order_count = 6
    assert await order_service.is_nth_order() is True


@pytest.mark.asyncio
async def test_get_order_summary(order_service):
    await order_service.place_order([], 100.0, 10.0, "DISCOUNT1")
    await order_service.place_order([], 50.0, 0.0, None)

    summary = await order_service.get_order_summary()
    assert summary["total_orders"] == 2
    assert summary["total_purchase_amount"] == 150.0
    assert summary["total_discount_amount"] == 10.0
    assert len(summary["orders"]) == 2