import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

def create_stripe_product(name: str) -> str:
    try:
        product = stripe.Product.create(
            name=name,
            type="service"
        )
        return product.id
    except stripe.error.StripeError as e:
        raise Exception(f"Ошибка при создании продукта: {str(e)}")

def create_stripe_price(product_id: str, amount: float, currency: str = "rub") -> str:
    try:
        price = stripe.Price.create(
            product=product_id,
            unit_amount=int(amount * 100),
            currency=currency,
            recurring=None
        )
        return price.id
    except stripe.error.StripeError as e:
        raise Exception(f"Ошибка при создании цены: {str(e)}")

def create_stripe_checkout_session(price_id: str, success_url: str, cancel_url: str) -> dict:
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price": price_id,
                    "quantity": 1,
                }
            ],
            mode="payment",
            success_url=success_url,
            cancel_url=cancel_url,
        )
        return {"url": session.url, "session_id": session.id}
    except stripe.error.StripeError as e:
        raise Exception(f"Ошибка при создании сессии: {str(e)}")

def retrieve_stripe_session(session_id: str) -> dict:
    try:
        session = stripe.checkout.Session.retrieve(session_id)
        return {
            "status": session.payment_status,
            "session_id": session.id
        }
    except stripe.error.StripeError as e:
        raise Exception(f"Ошибка при получении информации о сессии: {str(e)}")