from app.services.order_service import order_service
from app.services.discount_service import discount_service

class AdminService:
    async def get_order_stats(self):
        """Returns order stats for admin overview."""
        return await order_service.get_order_summary()

    async def get_discount_codes(self):
        """Lists all available (unused) discount codes."""
        available_codes = [code for code, valid in discount_service.discount_code.items() if valid]
        return {"available_discount_codes": available_codes}

admin_service = AdminService()
