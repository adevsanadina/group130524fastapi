from fastapi import FastAPI


app = FastAPI()
from fastapi import FastAPI, status

app = FastAPI()
from schemas import NewProduct, SavedProduct
from storage import storage

app = FastAPI(
    debug=True,
    title='Group1305'
)

@app.get('/')

@app.get('/', include_in_schema=False)
def index():
    return 'Hello guys!'
    return {'subject': 'Hello!'}


# CRUD
@app.post('/api/product/', description='create product', status_code=status.HTTP_201_CREATED, tags=['API', 'Product'])
def add_product(new_product: NewProduct) -> SavedProduct:
    saved_product = storage.create_product(new_product)
    return saved_product
 15 changes: 15 additions & 0 deletions15
schemas.py
