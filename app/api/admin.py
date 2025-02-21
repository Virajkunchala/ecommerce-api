from fastapi import APIRouter
from app.services.admin_service import admin_service

router = APIRouter()

@router.get("/orders")
async def get_order_stats():
    """Returns total orders, purchase amount, and discount amount."""
    return await admin_service.get_order_stats()

@router.get("/discounts")
async def get_available_discounts():
    """Returns all available (unused) discount codes."""
    return await admin_service.get_discount_codes()
