from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Couple(Base):
    __tablename__ = "couples"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String(32), unique=True, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    users = relationship("User", back_populates="couple")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(Integer, unique=True, nullable=False)
    couple_id = Column(Integer, ForeignKey("couples.id"), nullable=True)
    created_at = Column(DateTime, server_default=func.now())

    couple = relationship("Couple", back_populates="users")
