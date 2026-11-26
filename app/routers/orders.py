from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Order, OrderItem, Product, Customer, User
from app.schemas import OrderCreate, OrderOut
from app.auth import get_current_user, require_admin
from app.tasks import send_order_notification

router = APIRouter(prefix="/orders", tags=["orders"])

@router.post("/", response_model=OrderOut)
def create_order(data: OrderCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    customer = db.query(Customer).filter(Customer.id == data.customer_id).first()
    if not customer:
        raise HTTPException(404, "Покупатель не найден")
    if not data.items:
        raise HTTPException(400, "Заказ должен содержать хотя бы один товар")

    order = Order(customer_id=customer.id)
    db.add(order)
    db.flush()

    total = 0.0
    for item in data.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if not product:
            raise HTTPException(404, f"Продукт {item.product_id} не найден")
        if product.stock < item.quantity:
            raise HTTPException(400, f"Недостаточно товара на складе: {product.name}")
        product.stock -= item.quantity
        total += product.price * item.quantity
        db.add(OrderItem(order_id=order.id, product_id=product.id, quantity=item.quantity))

    db.commit()
    db.refresh(order)

    send_order_notification.delay(order.id, customer.email, total)
    return order

@router.get("/", response_model=list[OrderOut])
def list_orders(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Order).all()

@router.get("/all", response_model=list[OrderOut], dependencies=[Depends(require_admin)])
def list_all_orders(db: Session = Depends(get_db)):
    return db.query(Order).all()

@router.get("/{order_id}", response_model=OrderOut)
def get_order(order_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(404, "Заказ не найден")
    return order