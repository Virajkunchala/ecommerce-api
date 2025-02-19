from typing import List, Dict
from pydantic import BaseModel
from fastapi import HTTPException

class CartService:
    def __init__(self):
        self.cart_items: List[Dict[str, int]] = []
        self.order_count=0
        
    async def add_to_cart(self,product_id: int, quantity: int):
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
        return self.cart_items
    
    
    async def checkout(self,discount_code:str=None):
        
        self.order_count+=1
        
        if self.order_count %5 == 0 and discount_code =='DISCOUNT10':
            return {"message": "Order placed successfully with 10% discount!"}
        elif self.order_count % 5 != 0:
            return {"message": "Order placed successfully, no discount applied."}
        else:
            raise HTTPException(status_code=400, detail="Invalid discount code")
            
    
    
# cart_service = CartService()
