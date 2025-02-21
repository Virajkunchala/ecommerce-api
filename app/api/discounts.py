from fastapi import APIRouter, HTTPException
from app.services.discount_service import discount_service

router = APIRouter()

@router.get("/discounts")
async def get_available_discounts():
    """Returns all available (unused) discount codes."""
    available_codes = [code for code, valid in discount_service.discount_codes.items() if valid]
    return {"available_discount_codes": available_codes}

@router.get("/discounts/{discount_code}")
async def validate_discount(discount_code: str):
    """Validates if a discount code is available and can be used."""
    try:
        await discount_service.validate_discount_code(discount_code)
        return {"message": "Discount code is valid and can be applied"}
    except HTTPException as e:
        raise e
