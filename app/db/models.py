from enum import Enum
from sqlalchemy import (
    Column, Integer, String, Text, DECIMAL, ForeignKey,
    TIMESTAMP, CheckConstraint, func, Enum as SqlEnum,Boolean,DateTime
)
from sqlalchemy.orm import relationship

from app.db.database import Base


class UserRoles(str, Enum):
    ADMIN = "admin"
    USER = "user"


class OrderStatus(str, Enum):
    PENDING = "pending"
    PAID = "paid"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"
    COMPLETED = "completed"

                                                                              
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    phone = Column(String(20), unique=True)
    password = Column(String(255), nullable=False)
    age = Column(Integer, CheckConstraint("age >= 0"))
    role = Column(SqlEnum(UserRoles), default=UserRoles.USER, nullable=False)
    is_verified = Column(Boolean,default=False,nullable=False)
    verification_code = Column(String, nullable=True)
    code_expires = Column(DateTime, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

    orders = relationship("Order", back_populates="user", cascade="all, delete")


class Venue(Base):
    __tablename__ = "venues"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    lon = Column(DECIMAL(9, 6), nullable=False)
    lat = Column(DECIMAL(9, 6), nullable=False)

    events = relationship("Event", back_populates="venue", cascade="all, delete")


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    description = Column(Text)
    limit_age = Column(Integer, CheckConstraint("limit_age >= 0"))
    venue_id = Column(Integer, ForeignKey("venues.id", ondelete="CASCADE"))
    start_time = Column(TIMESTAMP(timezone=True), nullable=False)
    end_time = Column(TIMESTAMP(timezone=True))

    venue = relationship("Venue", back_populates="events")
    tickets = relationship("Ticket", back_populates="event", cascade="all, delete")


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    event_id = Column(Integer, ForeignKey("events.id", ondelete="CASCADE"))
    price = Column(DECIMAL(10, 2), CheckConstraint("price >= 0"))
    quantity = Column(Integer, CheckConstraint("quantity >= 0"))

    event = relationship("Event", back_populates="tickets")
    orders = relationship("Order", back_populates="ticket", cascade="all, delete")


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    ticket_id = Column(Integer, ForeignKey("tickets.id", ondelete="CASCADE"))
    quantity = Column(Integer, CheckConstraint("quantity > 0"))
    status = Column(SqlEnum(OrderStatus), default=OrderStatus.PENDING, nullable=False)
    total_price = Column(DECIMAL(10, 2), CheckConstraint("total_price >= 0"))
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())
    
    user = relationship("User", back_populates="orders")
    ticket = relationship("Ticket", back_populates="orders")
