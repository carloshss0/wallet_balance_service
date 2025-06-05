from sqlalchemy import Column, String, Float
from .db import Base

class Balance(Base):
    __tablename__ = "balances"

    account_id = Column(String, primary_key=True, index=True)
    balance = Column(Float, default=0.0)


    def __repr__(self):
        return f"Balance(account_id={self.account_id}, balance={self.balance})"
