# Ecommerce Store API

 E-commerce store API built with FastAPI.

## Features:

*   **Cart Management:** Add, view, remove items from cart.
*   **Checkout:**  Checkout with optional discount code.
*   **Discount Codes:**
    *   Automatic discount code generation for every 5th order.
    *   Discount code validation during checkout.
    *   Admin API to generate discount codes manually.
*   **Admin Stats:** API to view store data (discount code usage, etc.).

## How to Run:

1.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
2.  **Run the application:**
    ```bash
    uvicorn app.main:app --reload
    ```

## API Endpoints:

**Cart API:**

*   `GET /api/cart/add`: Add items to cart(request body: `Product_id`  and `quantity`).
*   `GET /api/cart/`: Display the cart .
*   `DELETE /api/cart/clear`: Clear the cart.

**Checkout API:**

*   `POST /api/checkout/{user_id}?discount_code={code}`: Checkout cart with optional discount code.

**Discount API (Admin):**

*   `POST /api/admin/discount/generate`: Generate a new discount code (admin only).

**Admin API:**

*   `GET /api/admin/stats`: Get store statistics (admin only).


## Using the API (Example with `curl` or Postman/REST Client):**

**Add item to cart:**
```bash
curl -X POST "[http://127.0.0.1:8000/api/cart/add?quantity=2]" \
-H "Content-Type: application/json" \
-d '{
    "product_id": "2",
    "name": "Product 1",
}'