from app.celery_app import celery_app

@celery_app.task
def send_order_notification(order_id: int, customer_email: str, total: float):
    print(f"[УВЕДОМЛЕНИЕ] Создан заказ #{order_id} для {customer_email}, сумма={total}")
    return {"order_id": order_id, "status": "уведомление_отправлено"}