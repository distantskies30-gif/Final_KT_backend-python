from pydantic import BaseModel
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    role: str
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class CustomerCreate(BaseModel):
    full_name: str
    email: str
    phone: str = ""

class CustomerOut(BaseModel):
    id: int
    full_name: str
    email: str
    phone: str
    class Config:
        from_attributes = True

class ProductCreate(BaseModel):
    name: str
    price: float
    stock: int = 0

class ProductOut(BaseModel):
    id: int
    name: str
    price: float
    stock: int
    class Config:
        from_attributes = True

class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int = 1

class OrderItemOut(BaseModel):
    id: int
    product_id: int
    quantity: int
    class Config:
        from_attributes = True

class OrderCreate(BaseModel):
    customer_id: int
    items: list[OrderItemCreate]

class OrderOut(BaseModel):
    id: int
    customer_id: int
    status: str
    created_at: datetime
    items: list[OrderItemOut]
    class Config:
        from_attributes = True