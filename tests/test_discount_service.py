import pytest
from app.services.discount_service import DiscountService

@pytest.fixture
def discount_service():
    # DiscountService with nth_order=3 for testing 
    return DiscountService(nth_order=3, discount_percentage=10.0)

@pytest.mark.asyncio
async def test_generate_discount_code_always_generates_code(discount_service): 
    # Reset order count 
    discount_service.order_count = 0

    code1 = await discount_service.generate_discount_code()
    code2 = await discount_service.generate_discount_code()
    code3 = await discount_service.generate_discount_code()

    assert code1 is not None 
    assert isinstance(code1, str)
    assert code1 in discount_service.discount_codes
    assert discount_service.discount_codes[code1] is True

    assert code2 is not None
    assert isinstance(code2, str)
    assert code2 in discount_service.discount_codes
    assert discount_service.discount_codes[code2] is True

    assert code3 is not None
    assert isinstance(code3, str)
    assert code3 in discount_service.discount_codes
    assert discount_service.discount_codes[code3] is True

@pytest.mark.asyncio
async def test_generate_discount_code(discount_service):
    discount_code = await discount_service.generate_discount_code()
    assert discount_code is not None
    assert isinstance(discount_code, str)
    assert discount_code in discount_service.discount_codes
    assert discount_service.discount_codes[discount_code] is True


@pytest.mark.asyncio
async def test_validate_valid_discount_code(discount_service):
    valid_code = await discount_service.generate_discount_code() # Generate a valid code
    is_valid = await discount_service.validate_discount_code(valid_code)
    assert is_valid is True

@pytest.mark.asyncio
async def test_validate_invalid_discount_code(discount_service):
    is_valid = await discount_service.validate_discount_code("INVALID_CODE")
    assert is_valid is False

@pytest.mark.asyncio
async def test_apply_discount_valid_code(discount_service):
    valid_code = await discount_service.generate_discount_code()
    total_amount = 100.0
    discount_amount = await discount_service.apply_discount(total_amount, valid_code)
    assert discount_amount == 10.0

@pytest.mark.asyncio
async def test_apply_discount_invalid_code(discount_service):
    total_amount = 100.0
    discount_amount = await discount_service.apply_discount(total_amount, "INVALID_CODE")
    assert discount_amount == 0.0

@pytest.mark.asyncio
async def test_mark_discount_as_used(discount_service):
    valid_code = await discount_service.generate_discount_code()
    await discount_service.mark_discount_as_used(valid_code)
    assert discount_service.discount_codes[valid_code] is False 
    is_valid_after_use = await discount_service.validate_discount_code(valid_code)
    assert is_valid_after_use is False 

@pytest.mark.asyncio
async def test_get_available_discounts(discount_service):
    # Generate two valid codes
    code1 = await discount_service.generate_discount_code()
    code2 = await discount_service.generate_discount_code()
    # Use one code
    await discount_service.mark_discount_as_used(code1)

    available_discounts = discount_service.get_available_discounts()
    assert code2 in available_discounts
    assert code1 not in available_discounts 
    assert len(available_discounts) == 1