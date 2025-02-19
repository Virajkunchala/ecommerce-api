from typing import List, Dict
from pydantic import BaseModel
from fastapi import HTTPException

class CartService:
    def __init__(self):
        self.cart_items: List[Dict[str, int]] = []
        self.order_count=0
        
    async def add_to_cart(self,product_id: int, quantity: int):
        """Adds an item to the cart or updates the exsisting quantity"""
        if quantity <=0:
            raise HTTPException(status_code=400,detail='Quantity must be gretar than 0')
        
        for item in self.cart_items:
            if item['product_id']==product_id:
                item['quantity']+=quantity
                return self.cart_items
            
        
         # if there is no product add new item
        new_item = {"product_id": product_id, "quantity": quantity}
        self.cart_items.append(new_item)
        return self.cart_items

    async def get_cart_items(self):
        """
        Returns the cart description
        """
        return self.cart_items
    
    async def clear_cart(self):
        """Clear the cart after checkout."""
        return self.cart_items;
    
 #singleton Instance to manage the state   
cart_service=CartService()