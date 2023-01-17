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
    host="redis-16564.c212.ap-south-1-1.ec2.cloud.redislabs.com",
    port=16564,
    password="962RobFvdBZoPeUilJIfKS9GnWDYj6gh",
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
