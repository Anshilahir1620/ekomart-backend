from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.database import Base, engine

# models
from app.models.users import User
from app.models.roles import Role
from app.models.brands import Brand
from app.models.banners import Banner
from app.models.categories import Category
from app.models.products import Product
from app.models.subcategories import SubCategory
from app.models.cart import Cart, CartItem
from app.models.daily_offer import DailyOffer

# routers
from app.api.user import router as user_router
from app.api.Categories import router as category_router
from app.api.Subcategories import router as subcategory_router
from app.api.Brand import router as brand_router
from app.api.Banners import router as banner_router
from app.api.Products import router as product_router
from app.api.Roles import router as roles_router
from app.api.auth import router as auth_router
from app.api.cart import router as cart_router
from app.api.Order import router as order_router
from app.api.payment import router as payment_router
from app.api.Coupons import router as coupons_router
from app.api.admin import router as admin_router
from app.api.daily_offer import router as daily_offer_router
from app.api.search import router as search_router


Base.metadata.create_all(bind=engine)

app = FastAPI(title="My Backend")


@app.get("/")
def root():
    return {"message": "API Running"}


app.mount(
    "/public",
    StaticFiles(directory="app/public"),
    name="public"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://ekomart-frontend.vercel.app",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)
app.include_router(category_router)
app.include_router(subcategory_router)
app.include_router(brand_router)
app.include_router(banner_router)
app.include_router(product_router)
app.include_router(roles_router)
app.include_router(auth_router)
app.include_router(cart_router)
app.include_router(order_router)
app.include_router(payment_router)
app.include_router(coupons_router)
app.include_router(admin_router)
app.include_router(daily_offer_router)
app.include_router(search_router)
