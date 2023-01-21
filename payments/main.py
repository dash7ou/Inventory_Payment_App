from fastapi import FastAPI, Response
from redis_om import get_redis_connection, HashModel, NotFoundError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.background import BackgroundTasks
from starlette.requests import Request
import requests
from pydantic import BaseModel
import time


inventory_url = "http://localhost:8000"

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


class Order(HashModel):
    product_id: str
    price: float
    fee: float
    total: float
    quantity: int
    status: str

    class Meta:
        database = redis


class CreateOrder(BaseModel):
    product_id: str
    quantity: int


@app.get("/order/{id}")
def get_order(id: str):
    return Order.get(id)

@app.post("/orders")
def create(order: CreateOrder, background_tasks: BackgroundTasks):
    request_url = inventory_url + "/products/" + order.product_id
    req = requests.get(request_url)
    product = req.json()

    order = Order(
        product_id=order.product_id,
        price=product["price"],
        fee=0.2 * product["price"],
        total=1.2 * product["price"],
        quantity=product["quantity"],
        status="pending",
    )

    order.save()

    background_tasks.add_task(order_compeleted, order)

    return order



def order_compeleted(order: Order):
    time.sleep(5)
    order.status = "compeleted"
    order.save()
    # * mean auto generated ID.
    redis.xadd('order_completed', order.dict(), '*')