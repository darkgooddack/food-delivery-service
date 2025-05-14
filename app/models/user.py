import enum

from sqlalchemy import Column, Integer, String, Enum
from app.db.init_db import Base

class UserRole(enum.Enum):
    user = "user"
    courier = "courier"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    telephone = Column(String)
    address = Column(String)
    role = Column(Enum(UserRole), nullable=False, default=UserRole.user)