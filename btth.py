from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI()

products = [
    {"id": 1, "name": "Keyboard", "price": 500000},
    {"id": 2, "name": "Mouse", "price": 300000}
]


class ProductCreate(BaseModel):
    name: str
    price: float


@app.post("/products", status_code=status.HTTP_201_CREATED)
def create_product(product: ProductCreate):
    if not product.name.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product name must not be empty"
        )

    if product.price <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Price must be greater than 0"
        )

    new_product = {
        "id": len(products) + 1,
        "name": product.name,
        "price": product.price
    }
    products.append(new_product)
    return new_product


@app.get("/products")
def get_products():
    return products


@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    target_product = next((p for p in products if p["id"] == product_id), None)
    if target_product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    products.remove(target_product)
    return {
        "message": "Product deleted successfully",
        "data": target_product
    }