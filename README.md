# Ecommerce Store API

## Overview

E-commerce store API built with FastAPI.

---

## Features

The application uses an in-memory store to manage the following:

- **Cart Management**: Stores the list of items added to the cart.
-**Checkout**:Checkout with optional discount code.
-**Discount Codes**:
    Automatic discount code generation for every nth order(Assumed n=3).
    Discount code validation during checkout.
- **Orders**: Stores details of placed orders, including total amounts and applied discounts.

---

## API Endpoints

### 1. Add Item to Cart  
**Endpoint**: `/cart/items`  
**Method**: `POST`

**Description**: Adds an item to the cart with the specified `product_id` and `quantity`. 
The prices have been hardcoded to simplify the implementation, as they were not specified in the documentation.

## 🛒 Valid Product IDs & Prices

| Product ID | Price (₹) |
|------------|---------|
| 1          | 100     |
| 2          | 200     |
| 3          | 50      |
| 4          | 150     |
| 5          | 400     |

🔹 Make sure to use **only the product IDs listed above** when adding items to the cart. 

**Request Body (JSON)**:
```json
{
    "product_id": 1,
    "quantity": 2
}

```


Response (Success):

```json
{
    "message": "Item added to cart",
    "cart": {
        "cart": [
            {
                "product_id": 1,
                "quantity": 2,
                "price": 100
            }
        ]
    }
}
```

## 2. View Cart
Endpoint: /cart
Method: GET

Description: Fetches the current contents of the user's cart, including product details (id, quantity, price).

Response (Success):

```json
{
    "cart": [
        {
            "product_id": 1,
            "quantity": 2,
            "price": 100
        }
    ]
}
  ```

## 3. Checkout
When the user reaches their nth(I Assumed n=3) order, a coupon code is generated. This coupon can be applied at checkout but is valid for one-time use only.

Endpoint: /order/checkout
Method: POST

Description: Finalizes the order, calculates the total amount, and applies any valid discount codes.

Request Body (JSON):(with out discount code)

```json
{}
```
if nth order is not reached 
Response (Success):

```json
{
    "message": "Order placed successfully",
    "order_id": 3,
    "total_amount": 200,
    "discount_applied": 10,
    "discount_code": "null"
}
  ```

  Request Body (JSON):(with discount code)

```json
{
    "discount_code": "VALID_DISCOUNT_CODE"
}
```

Response (Success):

```json
{
    "message": "Order placed successfully",
    "order_id": 7,
    "total_amount": 180.0,
    "discount_applied": 20.0,
    "discount_code": "VALID_DISCOUNT_CODE",
    "new_discount_code_generated": "NEW_CODE_GENERATED_FOR_NEXT_NTH_ORDER"
}
  ```

## 4. Admin: View Orders and Statistics
Endpoint: /admin/orders
Method: GET

Description: Provides an overview of all orders, including the total count, total purchase amount, total discount amount, and available discount codes.

Response (Success):

```json
{
    "total_orders": 1,
    "total_purchase_amount": 200,
    "total_discount_amount": 10,
    "orders": [
        {
            "order_id": 1,
            "items": [
                {
                    "product_id": 1,
                    "quantity": 2,
                    "price": 100
                }
            ],
            "total_amount": 200,
            "discount_applied": 10,
            "discount_code": "19H9H0XWTI"
        }
    ]
}
  ```

## 5. Admin:Avilble discount codes (unused)
Endpoint: /admin/discounts
Method: POST

Description: Generates a new discount code for every nth order placed by a customer.

Response (Success):

```json
{
    "available_discount_codes": [
        "19H9H0XWTI"
    ]
}
```

## Assumptions
No Backend Store: The data is stored in memory and will be lost once the server is restarted...

Discount Code Usage: Discount codes can only be used once per customer and are generated after every nth order.

## Testing
The project includes unit tests to validate the functionality of the application. To run the tests, use the following command:

  ```bash

pytest tests/

  ```

Install Dependencies

  ```bash

pip install -r requirements.txt

  ```

Start the Application
To run the FastAPI server locally:
  ```bash
uvicorn main:app --reload

  ```

After the server is running, you can interact with the endpoints using tools like curl, Postman, or any REST client.