from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db
from models.payment import Payment

router = APIRouter()

@router.post("/create-payment-intent")
async def create_payment_intent(
    amount: float,
    tax_form_id: int,
    user_id: int = 1,
    db: Session = Depends(get_db)
):
    """Create a payment intent for tax filing fees"""
    # In production: create Stripe payment intent
    fake_payment_intent_id = f"pi_fake_{tax_form_id}"

    new_payment = Payment(
        user_id=user_id,
        tax_form_id=tax_form_id,
        stripe_payment_intent_id=fake_payment_intent_id,
        amount=amount,
        status="pending"
    )
    db.add(new_payment)
    db.commit()
    db.refresh(new_payment)

    return {
        "payment_intent_id": fake_payment_intent_id,
        "client_secret": "fake_client_secret",
        "amount": amount
    }

@router.get("/")
async def get_payments(user_id: int = 1, db: Session = Depends(get_db)):
    """Get all payments for user"""
    payments = db.query(Payment).filter(Payment.user_id == user_id).all()
    return [
        {
            "id": payment.id,
            "amount": float(payment.amount),
            "status": payment.status,
            "created_at": payment.created_at
        }
        for payment in payments
    ]

@router.post("/webhook")
async def stripe_webhook():
    """Handle Stripe webhook events"""
    # In production: verify webhook signature and process events
    return {"message": "Webhook received"}
