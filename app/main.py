from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from app.routers import auth_router, customers, products, orders
from app.routers.auth_router import limiter

app = FastAPI(title="КТ6. Финальный проект — Магазин")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://your-frontend.railway.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.include_router(auth_router.router)
app.include_router(customers.router)
app.include_router(products.router)
app.include_router(orders.router)

@app.get("/")
def root():
    return {"status": "ок"}