from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(128), nullable=False)
    number = Column(String(64), unique=True, nullable=False, index=True)
    balance = Column(Float, nullable=False, default=0.0)

    def to_dict(self):
        return {"id": self.id, "name": self.name, "number": self.number, "balance": float(self.balance)}
