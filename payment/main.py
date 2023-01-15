from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection, HashModel
from starlette.requests import Request
import requests

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
    product_id : str
    price : str
    fee : float
    total : float
    quantity : int
    status : str

    class Meta:
        database = redis

@app.post('/orders')
async def create_order(request : Request):
    body = await request.json()
    req = requests.get("http://localhost/products/%s" % body['id'])
    return request.json()