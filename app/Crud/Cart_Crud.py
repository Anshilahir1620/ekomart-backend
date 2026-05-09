from sqlalchemy.orm import Session
from app.models.cart import Cart, CartItem
from app.schemas.Cart_schema import CartItemCreate
from app.models.products import Product


def get_all_cart(db: Session):
    return db.query(Cart).all()



def get_cart_items(db: Session, user_id: int):

    cart = db.query(Cart).filter(Cart.user_id == user_id).first()

    if not cart:
        return {"items": [], "cart_total": 0}

    items_data = []
    total = 0

    for item in cart.items:

        product = db.query(Product).filter(Product.id == item.product_id).first()

        price = float(item.price_at_time)
        subtotal = price * item.quantity

        total += subtotal

        items_data.append({
            "product_id": item.product_id,
            "name": product.product_name,
            "price": price,
            "quantity": item.quantity,
            "subtotal": subtotal
        })

    return {
        "items": items_data,
        "cart_total": total
    }


def get_cart_by_id(db: Session, cart_id: int):
    return db.query(Cart).filter(Cart.id == cart_id).first()


def get_or_create_cart(db: Session, user_id: int):

    cart = db.query(Cart).filter(Cart.user_id == user_id).first()

    if not cart:
        cart = Cart(user_id=user_id)
        db.add(cart)
        db.commit()
        db.refresh(cart)

    return cart


def add_to_cart(db: Session, cart_id: int, item: CartItemCreate):

    cart_item = (
        db.query(CartItem)
        .filter(
            CartItem.cart_id == cart_id,
            CartItem.product_id == item.product_id).first()  )

    product = db.query(Product).filter(Product.id == item.product_id).first()

    if not product:
        return None

    price = product.sale_price or product.regular_price

    if cart_item:
        cart_item.quantity += item.quantity
    else:
        cart_item = CartItem(
            cart_id=cart_id,
            product_id=item.product_id,
            quantity=item.quantity,
            price_at_time= price
        )
        db.add(cart_item)

    db.commit()
    db.refresh(cart_item)

    return cart_item.cart