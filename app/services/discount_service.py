from typing import Dict,Optional
from fastapi import HTTPException

class DiscountService:
    def __init__(self,nth_order=5):
        self.discount_code:Dict[str,bool]={}
        self.nth_order=nth_order
                
    async def generate_discount_code(self,order_number:int)->Optional[str]:
        """Generate discount code for the order"""
        
        if order_number % self.nth_order == 0:
            discount_code = f"DISCOUNT{order_number}"
            self.discount_codes[discount_code] = True  # Mark as valid
            return discount_code
        return None
    
    async def validate_discount_code(self,discount_code: str) -> bool:
        """Checks if the discount code is valid and marks it as used."""
        if discount_code not in self.discount_codes or not self.discount_codes[discount_code]:
            raise HTTPException(status_code=400, detail="Invalid or expired discount code")

        # Mark the code as used
        self.discount_codes[discount_code] = False
        return 10.0 ##for fixed discount
    
discount_service = DiscountService()
        