from typing import List, Dict,Any
from pydantic import BaseModel
from fastapi import HTTPException

PRODUCT_PRICES = {1: 100, 2: 200, 3: 50}  # Product price lookup


class CartService:
    def __init__(self):
        self.cart_items: List[Dict[str, Any]] = []
        self.order_count=0
        
    async def add_to_cart(self,product_id: int, quantity: int):
        """Adds an item to the cart or updates the exsisting quantity"""
        if product_id not in PRODUCT_PRICES:
            raise HTTPException(status_code=400, detail="Invalid product ID")
        
        if quantity <=0:
            raise HTTPException(status_code=400, detail="Quantity must be greater than 0")

        price = PRODUCT_PRICES[product_id]  # Fetch price from lookup
        
        for item in self.cart_items:
            if item['product_id']==product_id:
                item['quantity']+=quantity
                return {"cart": self.cart_items}
            
        
         # if there is no product add new item
        new_item = {"product_id": product_id, "quantity": quantity,"price":price}
        self.cart_items.append(new_item)
        return {"cart": self.cart_items}


    async def get_cart_items(self):
        """
        Returns the cart description
        """
        return {"cart": self.cart_items}
    
    async def clear_cart(self):
        """Clear the cart after checkout."""
        self.cart_items=[];
        return {"message": "Cart cleared successfully"}
    
 #singleton Instance to manage the state   
cart_service=CartService()