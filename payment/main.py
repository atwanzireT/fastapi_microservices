from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection, HashModel
from starlette.requests import Request
import requests
from time import time

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["http://localhost:3000"],
    allow_methods = ['*'],
    allow_headers = ['*'],
)

# This should be a different database
redis = get_redis_connection(
    host = "redis-16375.c15.us-east-1-4.ec2.cloud.redislabs.com",
    port = 16375,
    password = "8kXmP1VOk9kYXbnOfIkGMrlo6vaZOgvG",
    decode_responses = True,
)

class Order(HashModel):
    product_id: str
    price: float
    fee: float
    total: float
    quantity: int
    status: str  # pending, completed, refunded

    class Meta:
        database = redis

@app.post('/orders')
async def create_order(request : Request): # id Quantity
    body = await request.json()
    req = requests.get('http://localhost:8000/products/%s' % body['id'])
    product = req.json()

    
    order = Order(
        product_id=body['id'],
        price=product['price'],
        fee=0.2 * product['price'],
        total=1.2 * product['price'],
        quantity=body['quantity'],
        status='pending'
    )
    order.save()
    order_completed(order)
    return order

def order_completed(order: Order):
    time.sleep(5)
    order.status = 'completed'
    order.save()
    # redis.xadd('order_completed', order.dict(), '*')