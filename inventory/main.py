from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection, HashModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["http://localhost:3000"],
    allow_methods = ['*'],
    allow_headers = ['*'],

)

redis = get_redis_connection(
    host = "redis-16375.c15.us-east-1-4.ec2.cloud.redislabs.com",
    port = 16375,
    password = "8kXmP1VOk9kYXbnOfIkGMrlo6vaZOgvG",
    decode_responses = True,

)

class Product(HashModel):
    name : str
    price : float
    quantity : int

    class Meta:
        database = redis

@app.get('/')
async def root():
    return {"message" : "Welcome to my api"}

@app.get('/products')
async def all_product():
    return [format(pk) for pk in Product.all_pks()]

def format(pk : str):
    product = Product.get(pk)

    return {
        "id" : product.pk,
        "name" : product.name,
        "price" : product.price,
        "quantity" : product.quantity
    }

@app.post('/products')
async def create_product(product : Product):
    return product.save()

@app.get('/product/{pk}')
async def get_product(pk : str):
    return Product.get(pk)
    
@app.delete('/products/{pk}')
async def delete_product(pk : str):
    return Product.get(pk).delete()