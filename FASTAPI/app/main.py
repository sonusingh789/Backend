from fastapi import FastAPI,HTTPException,Query,Path
from service.products import get_all_products
from schema.product import Product
app = FastAPI()

@app.get("/")
def root():
    return {"message ": "Welcome to FastAPI"}
    

# @app.get("/products")
# def get_products():
#     return get_all_products()

# Searching using Query
# @app.get("/products")
# def list_products(name:str=Query(default=None,min_length=1,max_length=50,description="Search by product name(case insensitive) ")):
#     products = get_all_products()
#     if name:
#         needle = name.strip().lower()
#         products = [p for p in products if needle in p.get("name","").lower() ]

#         if not products:
#             raise HTTPException(status_code=404, detail= f"No Product Found matching name={name}")
#         total = len(products)

#     return {"total":total,"items":products}

# Sorting ---------------------------------------------

# @app.get("/products")
# def list_products(name:str=Query(default=None,min_length=1,max_length=50,
# description="Search by product name(case insensitive) "),
# sort_by_price:bool = Query(
#     default=False, description="Sort Product by price"),
#     order:str = Query(
#     default="asc", description="Sort Order When Sort_by_price=true (asc,des)")
                  
#                   ):
#     products = get_all_products()
#     if name:
#         needle = name.strip().lower()
#         products = [p for p in products if needle in p.get("name","").lower() ]

#     if not products:
#         raise HTTPException(status_code=404, detail= f"No Product Found matching name={name}")
    
#     if sort_by_price:
#         reverse = order =="desc"
#         products = sorted(products,key=lambda p:p.get("price",0),reverse=reverse)

#     total = len(products)

#     return {"total":total,"items":products}

##pagination------------------

@app.get("/products")
def list_products(
    name: str = Query(
        default=None,
        min_length=1,
        max_length=50,
        description="Search by product name (case insensitive)"
    ),
    sort_by_price: bool = Query(
        default=False,
        description="Sort Product by price"
    ),
    order: str = Query(
        default="asc",
        description="Sort Order when sort_by_price=true (asc, desc)"
    ),
    limit: int = Query(
        default=10,
        ge=1,
        le=100,
        description="Number of items to return"
    ),
    # offset pagenumber concept
    offset: int = Query(
        default=0,
        ge=0,
        description="Pagination Offset"
    )
):
    products = get_all_products()

    if name:
        needle = name.strip().lower()
        products = [p for p in products if needle in p.get("name", "").lower()]

    if not products:
        raise HTTPException(
            status_code=404,
            detail=f"No Product Found matching name={name}"
        )

    if sort_by_price:
        reverse = order == "desc"
        products = sorted(products, key=lambda p: p.get("price", 0), reverse=reverse)

    total = len(products)

    # products = products[0:limit]
    products = products[offset:offset+limit]

    return {"total": total, "limit":limit, "items": products}

# DYNAMIC ROUTE- GET REQUEST 
@app.get("/products/{product_id}")
def get_product_by_id(
    product_id: str = Path(
        ...,
        min_length=36,
        max_length=36,
        description="UUID of the Product",
        example="excf-56ffs-ffgdhss5sfg",
    ),
):
    products =  get_all_products()
    for product in products:
        if product["id"] == product_id:
            return product
    raise HTTPException(status_code=404,detail="PRODUCT NOT FOUND") 



# unvalidated data 
# @app.post("/products",status_code=201)
# def create_products(product):
#     return product

# validting with pydantic
# BaseModel is a class  in pydantic  which provides validations.


             



@app.post("/products",status_code=201)
def create_products(product: Product):
    return product
