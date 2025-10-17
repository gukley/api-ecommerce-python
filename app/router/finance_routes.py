from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db

router = APIRouter(prefix="/api", tags=["Finance"])

@router.get("/payments")
def get_payments(db: Session = Depends(get_db)):
    # Exemplo: buscar pagamentos no banco (ajuste conforme seu modelo)
    payments = db.query(Payment).all()
    return [payment.to_dict() for payment in payments]
