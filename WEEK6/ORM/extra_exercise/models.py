from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker


Base = declarative_base()


engine = create_engine('sqlite:///orm_exercise.db', echo=False)


class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    
    
    addresses = relationship("Address", back_populates="user")
    automobiles = relationship("Automobile", back_populates="user")
    
    def __repr__(self):
        return f"<User(id={self.id}, name='{self.name}', email='{self.email}')>"



class Address(Base):
    __tablename__ = 'addresses'
    
    id = Column(Integer, primary_key=True)
    street = Column(String(200), nullable=False)
    city = Column(String(100), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    
    
    user = relationship("User", back_populates="addresses")
    
    def __repr__(self):
        return f"<Address(id={self.id}, street='{self.street}', city='{self.city}')>"



class Automobile(Base):
    __tablename__ = 'automobiles'
    
    id = Column(Integer, primary_key=True)
    brand = Column(String(50), nullable=False)
    model = Column(String(50), nullable=False)
    year = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))  
    
    
    user = relationship("User", back_populates="automobiles")
    
    def __repr__(self):
        return f"<Automobile(id={self.id}, brand='{self.brand}', model='{self.model}', year={self.year})>"



def validate_tables(engine):
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    
    print("\n📊 TABLE VALIDATION:")
    print("=" * 50)
    
    expected_tables = ['users', 'addresses', 'automobiles']
    
    for table in expected_tables:
        if table in tables:
            print(f"✅ Table '{table}' exists")
        else:
            print(f"❌ Table '{table}' DOES NOT exist - creating...")
            Base.metadata.create_all(engine)
            print(f"✅ Table '{table}' created")
    
    print("=" * 50)



if __name__ == "__main__":
    
    validate_tables(engine)
    Base.metadata.create_all(engine)
    
    print("\n✅ Database ready to use!")
    print(f"📁 Database file: orm_exercise.db")