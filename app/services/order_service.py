from typing import List, Dict,Optional
from pydantic import BaseModel
from fastapi import HTTPException

class OrderService:
    def __init__(self, nth_order_threshold=3):
        self.orders: List[Dict] = []
        self.order_count = 0
        self.total_purchase_amount = 0
        self.total_discount_amount = 0
        self.nth_order_threshold=nth_order_threshold

    async def place_order(self, cart_items: List[Dict[str, int]], total_amount: float, discount_applied: float,discount_code: Optional[str]):
        """Place the order and record details"""
        self.order_count += 1
        order_id = self.order_count
        
        # Store the order
        self.orders.append({
            "order_id": order_id,
            "items": cart_items,
            "total_amount": total_amount,
            "discount_applied": discount_applied,
            "discount_code": discount_code
        })

        # Update purchase info
        self.total_purchase_amount += total_amount
        self.total_discount_amount += discount_applied

        return {
            "message": "Order placed successfully",
            "order_id": order_id,
            "total_amount": total_amount,
            "discount_applied": discount_applied,
             "discount_code": discount_code
        }
        
    async def is_nth_order(self):
        """Check if the current order is eligible for a discount."""
        return self.order_count % self.nth_order_threshold == 0


    async def get_order_summary(self):
        """Return the order summary and discount"""
        return {
            "total_orders": self.order_count,
            "total_purchase_amount": self.total_purchase_amount,
            "total_discount_amount": self.total_discount_amount,
            "orders": self.orders
        }

order_service = OrderService()
