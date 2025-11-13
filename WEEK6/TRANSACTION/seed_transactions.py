"""
Seed data for transaction exercises
"""

from sqlalchemy.orm import sessionmaker
from models_transactions import Product, User, engine, Base


Session = sessionmaker(bind=engine)


def seed_test_data():
    """Create test data for transactions"""
    session = Session()
    
    try:
        
        Base.metadata.create_all(engine)
        
        
        existing_users = session.query(User).count()
        if existing_users > 0:
            print("\n⚠️  Test data already exists. Skipping seed...")
            return
        
        print("\n" + "="*60)
        print("🌱 SEEDING TEST DATA")
        print("="*60)
        
        
        users = [
            User(name="Juan Pérez", email="juan@example.com"),
            User(name="María García", email="maria@example.com"),
            User(name="Carlos López", email="carlos@example.com"),
        ]
        
        for user in users:
            session.add(user)
        
        session.flush()  
        print(f"\n✅ Created {len(users)} users")
        
        
        products = [
            Product(name="Laptop HP", price=899.99, stock=10),
            Product(name="Mouse Logitech", price=25.50, stock=50),
            Product(name="Teclado Mecánico", price=75.00, stock=30),
            Product(name="Monitor Samsung 24\"", price=199.99, stock=15),
            Product(name="Webcam HD", price=45.99, stock=25),
        ]
        
        for product in products:
            session.add(product)
        
        session.commit()
        print(f"✅ Created {len(products)} products")
        
        print("\n" + "="*60)
        print("✅ TEST DATA SEEDED SUCCESSFULLY")
        print("="*60)
        
    except Exception as e:
        session.rollback()
        print(f"❌ Error seeding data: {e}")
    finally:
        session.close()


if __name__ == "__main__":
    seed_test_data()