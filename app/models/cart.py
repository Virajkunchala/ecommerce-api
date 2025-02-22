from pydantic import BaseModel, validator, ValidationError

class CartItem(BaseModel):
    product_id: int
    quantity: int

    @validator('quantity')
    def check_quantity(cls, value):
        if value <= 0:
            raise ValueError('Quantity must be greater than 0')
        return value
