from fastapi import FastAPI, Response
from redis_om import get_redis_connection, HashModel, NotFoundError
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request
import requests
from pydantic import BaseModel


inventory_url = "http://localhost:8000"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],
    allow_methods=["*"],
    allow_headers=["*"]
)

redis = get_redis_connection(
    host="redis-17673.c212.ap-south-1-1.ec2.cloud.redislabs.com",
    port=17673,
    password="xothjUNPDtTeKfHN1tJlhjznlfE93xaH",
    decode_responses=True
)


class Order(HashModel):
    product_id: str
    price: float
    fee: float
    total: float
    quantity: int
    status: str

    class Meta:
        database: redis


class CreateOrder(BaseModel):
    product_id: str
    quantity: int


@app.post("/orders")
def create(order: CreateOrder):
    # request_url = inventory_url + "/products/" + order.product_id
    # req = requests.get(request_url)
    # product = req.json()

    # order = Order(
    #     product_id=order.product_id,
    #     price=product["price"],
    #     fee=0.2 * product["price"],
    #     total=1.2 * product["price"],
    #     quantity=product["quantity"],
    #     status="pending",
    # )

    order = Order(
        product_id="ccc",
        price=10,
        fee=0.2 * 10,
        total=1.2 * 10,
        quantity=5,
        status="pending",
    )

    order.save()

    return order
