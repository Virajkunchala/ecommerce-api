from typing import Dict, Optional
from fastapi import HTTPException
import string,random

class DiscountService:
    def __init__(self, nth_order=3,discount_percentage=10.0):
        self.discount_codes: Dict[str, bool] = {}  # Stores discount codes
        self.nth_order = nth_order
        self.order_count=0
        self.discount_percentage=discount_percentage

    async def generate_discount_code(self) -> Optional[str]:
        """
        Generates a discount code for every nth order.
        """
        discount_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        self.discount_codes[discount_code] = True
        return discount_code

    async def validate_discount_code(self, discount_code: str) -> float:
        """
        Checks if the discount code is valid and unused.

        """
        if discount_code  in self.discount_codes and self.discount_codes[discount_code]:
            return True        
        return False

    
    async def apply_discount(self, total_amount: float, discount_code: str) -> float:
        """Applies discount to the total amount if the code is valid."""
        if await self.validate_discount_code(discount_code):
            discount_amount = (self.discount_percentage / 100) * total_amount 
            return discount_amount
        return 0.0
    
    async def mark_discount_as_used(self, discount_code: str):
        """Marks the discount code as used after applying it."""
        if discount_code in self.discount_codes:
            self.discount_codes[discount_code] = False

    def get_available_discounts(self):
        """
        Returns a list of valid, unused discount codes.
        """
        return [code for code, valid in self.discount_codes.items() if valid]

discount_service = DiscountService()
