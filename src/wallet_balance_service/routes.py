from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from .db.db import SessionLocal
from .db.models import Balance

router = APIRouter()

@router.get("/balances/{account_id}")
def get_balance(account_id: str):
    db: Session = SessionLocal()
    balance = db.query(Balance).get(account_id)
    if not balance:
        raise HTTPException(status_code=404, detail="Account not found")
    return {"account_id": account_id, "balance": balance.balance}