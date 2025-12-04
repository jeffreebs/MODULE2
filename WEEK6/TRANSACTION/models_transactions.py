"""
Models for Transaction Exercises
Ejercicios de Transacciones - Modelos de base de datos
"""

from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, DateTime, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime
import enum


Base = declarative_base()


engine = create_engine('sqlite:///transactions.db', echo=False)


class InvoiceStatus(enum.Enum):
    """Enum for invoice status"""
    COMPLETED = "completed"
    RETURNED = "returned"
    PENDING = "pending"


class Product(Base):
    """Product model"""
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False, default=0)
    
    
    invoices = relationship("Invoice", back_populates="product")
    
    def __repr__(self):
        return f"<Product(id={self.id}, name='{self.name}', price={self.price}, stock={self.stock})>"


class User(Base):
    """User model"""
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    
    
    invoices = relationship("Invoice", back_populates="user")
    
    def __repr__(self):
        return f"<User(id={self.id}, name='{self.name}', email='{self.email}')>"


class Invoice(Base):
    """Invoice model"""
    __tablename__ = 'invoices'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    date = Column(DateTime, default=datetime.now)
    total = Column(Float, nullable=False)
    status = Column(Enum(InvoiceStatus), default=InvoiceStatus.COMPLETED)
    
    
    user = relationship("User", back_populates="invoices")
    product = relationship("Product", back_populates="invoices")
    
    def __repr__(self):
        return f"<Invoice(id={self.id}, user_id={self.user_id}, product_id={self.product_id}, quantity={self.quantity}, total={self.total}, status={self.status.value})>"



if __name__ == "__main__":
    print("\n" + "="*60)
    print("📦 CREATING TABLES FOR TRANSACTIONS")
    print("="*60)
    
    Base.metadata.create_all(engine)
    
    print("\n✅ Tables created successfully!")
    print("   - products")
    print("   - users")
    print("   - invoices")
    print("\n📁 Database file: transactions.db")