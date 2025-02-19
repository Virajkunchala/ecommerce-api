from fastapi import FastAPI, HTTPException
import uvicorn
from app.api import cart




app = FastAPI(title="E-commerce API")

app.include_router(cart.router,prefix='/cart',tags=["Cart"])


@app.get("/health")
async def main():
    return {"status": "running"}
    


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)  