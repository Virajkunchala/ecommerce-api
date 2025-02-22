from fastapi import FastAPI, HTTPException
import uvicorn
from app.api import cart,orders,discounts,admin




app = FastAPI(title="E-commerce API")

app.include_router(cart.router,prefix='/cart',tags=["Cart"])

app.include_router(orders.router,prefix='/order',tags=["Order"])

app.include_router(discounts.router,prefix='/discount',tags=["Discount"])


app.include_router(orders.router,prefix='/checkout',tags=["Checkout"])


app.include_router(admin.router,prefix='/admin',tags=["Admin"])




@app.get("/health")
async def main():
    return {"status": "running"}
    


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)  