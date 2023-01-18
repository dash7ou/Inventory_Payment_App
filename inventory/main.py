from fastapi import FastAPI, Response
from redis_om import get_redis_connection, HashModel, NotFoundError
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],
    allow_methods=["*"],
    allow_headers=["*"]
)

redis = get_redis_connection(
    host="localhost",
    port=6379,
    password="mohammed12345",
    decode_responses=True
)


class Product(HashModel):
    name: str
    price: float
    quantity: int

    class Meta:
        database = redis


def get_product_details(pk):
    product = Product.get(pk)
    return {
        'id': pk,
        'name': product.name,
        'price': product.price,
        'quantity': product.quantity
    }


@app.get("/products")
def all():
    return [get_product_details(pk) for pk in Product.all_pks()]


@app.get("/products/{id}")
def get_product(id: str, response: Response):
    try:
        return get_product_details(id)
    except NotFoundError:
        response.status_code = 404
        return {}
    except:
        response.status_code = 500
        return {
            "error": "Server Error!"
        }


@app.post("/products")
def create(product: Product, response: Response):
    try:
        return product.save()
    except:
        response.status_code = 500
        return {
            "error": "Server Error!"
        }


@app.delete("/products/{id}")
def delete_product(id: str, response: Response):
    try:
        get_product_details(id)
        return Product.delete(id)
    except NotFoundError:
        response.status_code = 404
        return {}
    except:
        response.status_code = 500
        return {
            "error": "Server Error!"
        }
