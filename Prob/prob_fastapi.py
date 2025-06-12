from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum

# FastAPI 애플리케이션 인스턴스 생성 
app = FastAPI(
    title = '상품 관리 API', 
    description = '상품 정보 관리하는 API'
)

# 카테고리 설정 위해 Enum(열거형) 클래스 설정 
# 미리 정의돈 고정된 값 목록 중 하나만 선택하게 만들 때 사용 -> 카테고리 중 하나를 선택하도록 할 때 유용하게 사용할 수 O
class CategoryEnum(str, Enum):
    electronics = "electronics"
    clothing = "clothing"
    books = "books"

# 상품 정보 관련 클래스 
# BaseModel을 통해 JSON 데이터를 자동으로 Python 객체로 변환 / 객체가 정의한 타입 조건과 제약 조건을 만족하는지 검사
# Field를 이용해 BaseModel 안에서 각 필드(변수)의 세부 제약 조건이나 설명ㅇㄹ 지정할 수 있게 해줌
class Product(BaseModel):
    id: int
    name: str = Field(..., min_length=2, max_length=100, description="상품명 (2-100자)")
    price: float = Field(..., gt=0, description="가격 (0보다 큰 수)")
    category: CategoryEnum = Field(..., description="카테고리")

# 상품 생성 관련 클래스 
class ProductCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, description="상품명 (2-100자)")
    price: float = Field(..., gt=0, description="가격 (0보다 큰 수)")
    category: CategoryEnum = Field(..., description="카테고리")

class ProductUpdate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, description="상품명 (2-100자)")
    price: float = Field(..., gt=0, description="가격 (0보다 큰 수)")
    category: CategoryEnum = Field(..., description="카테고리")

# 상품 데이터를 저장할 리스트 생성 (DB 대체)
products_db = []

# 생성된 상품에 할당할 ID를 위해 정의 
next_id = 1

# 루트 경로 API 엔드포인트
@app.get("/")
def read_root():
    """ API 루트 경로 """

    return {"message": "상품 관리 API입니다. "}

# 상품 생성 API 엔드포인트 
@app.post("/products", response_model=Product, status_code=201)
def create_product(product: ProductCreate):
    """ 상품을 생성합니다. """

    # global을 사용해 전역 변수를 함수 내에서 수정할 수 있도록 설정 
    global next_id

    # ProductCreate 모델의 데이터를 받아 새로운 Product 인스턴스를 생성 
    new_product = Product(
        id = next_id, 
        name = product.name,
        price = product.price,
        category = product.category
    )

    # 생성된 상품을 메모리 DB에 추가 
    products_db.append(new_product)
    # 다음 상품을 위해 ID 값을 1 증가 시킴 
    next_id += 1

    return new_product

# 상품 목록 조회 API 엔드포인트 
@app.get("/products", response_model=List[Product])
def get_products(
    category: Optional[CategoryEnum] = Query(None, description="카테고리를 이용해 필터링"),

    min_price: Optional[float] = Query(None, ge=0, description="Min Price"),
    max_price: Optional[float] = Query(None, ge=0, description="Max Price")
):

    """ 모든 상품을 조회합니다. """

    # 원본 데이터를 수정하지 않기 위해 복사본 생성 
    filtered_products = products_db.copy()

    # 카테고리 필터가 제공된 경우
    if category:
        # 리스트 컴프리헨션을 사용해 해당 카테고리의 상품들만 필터링
        # [조건을 만족하는 요소 for 요소 in 리스트 if 조건]
        filtered_products = [p for p in filtered_products if p.category == category]
    
    # 최소 가격 필터가 제공된 경우 (None이 아닌 경우)
    if min_price is not None:
        # 가격이 최소 가격 이상인 상품들만 필터링
        filtered_products = [p for p in filtered_products if p.price >= min_price]
    
    # 최대 가격 필터가 제공된 경우
    if max_price is not None:
        # 가격이 최대 가격 이하인 상품들만 필터링
        filtered_products = [p for p in filtered_products if p.price <= max_price]
    
    # 필터링된 상품 목록을 반환
    return filtered_products

# 특정 상품 조회 API 엔드포인트 
# {product_id}: URL 경로에서 변수 부분 
@app.get("/products/{product_id}", response_model=Product)
def get_product(product_id: int):
    """ 특정 상품을 조회합니다. """

    # 저장된 모든 상품을 순회하며 일치하는 ID 상품 조회 
    for product in products_db:
        # 상품의 ID와 요청된 ID 일치 여부 확인 
        if product.id == product_id:
            # 일치하면 해당 상품 정보 리턴 
            return product

    # 반복문이 종료 될때까지 상품을 찾지 못한 경우 
    # 404 Not Found 에러 리턴      
    raise HTTPException(status_code=404, detail="상품을 찾을 수 없습니다. ")

# 상품 정보 수정 API 엔드포인트 
# PUT 메서드: 전체 리소스 업데이터 사용 
@app.put("/products/{product_id}", response_model=Product)
def update_product(product_id: int, product_update: ProductUpdate):
    """ 기존 상품을 수정합니다. """

    # enumerate(): 인덱스와 값을 동시에 리턴하는 내장 함수 / 추후 리스트의 특정 위치 요소를 교체해야 하기에 인덱스가 필요 
    for i, product in enumerate(products_db):
        # 수정할 상품의 ID의 일치 여부 확인
        if product.id == product_id:
            update_data = product_update.dict(exclude_unset=True) # None이 아닌 값들만 딕셔너리에 포함 

            update_product = product.copy(update = update_data)
            products_db[i] = update_product

            return update_product
        
    raise HTTPException(status_code=404, detail="상품을 찾을 수 없습니다. ")

# 상품 삭제 API 엔드포인트
# DELETE 메서드 사용, response_model을 지정하지 X
@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    """ 상품을 삭제합니다. """
    
    for i, product in enumerate(products_db):
        if product.id == product_id:
            # pop(i): 리스트의 i번째 요소를 제거하고 해당 요소 리턴 
            delete_product = products_db.pop(i)

            return {"message": f"상품 '{delete_product.name}'이(가) 삭제되었습니다. "}
        
    raise HTTPException(status_code=404, detail="상품을 찾을 수 없습니다. ")

# 사용 가능한 카테고리 목록 조회 API 엔드포인트 
# response_model=List[str]: 문자열 리스트 리턴
@app.get("/categories", response_model=List[str])
def get_categories():
    """ 사용 가능한 모든 카테고리를 조회합니다. """

    # category.value: Enum의 실제 값
    return [category.value for category in CategoryEnum]