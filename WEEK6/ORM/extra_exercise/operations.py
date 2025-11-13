from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
from models import User, Address, Automobile, engine


Session = sessionmaker(bind=engine)
session = Session()


class UserOperations:
    """Class to manage user operations"""
    
    @staticmethod
    def create_user(name, email):
        """Create a new user"""
        new_user = User(name=name, email=email)
        session.add(new_user)
        session.commit()
        print(f"✅ User created: {new_user}")
        return new_user
    
    @staticmethod
    def update_user(user_id, name=None, email=None):
        """Update an existing user"""
        user = session.query(User).filter_by(id=user_id).first()
        if user:
            if name:
                user.name = name
            if email:
                user.email = email
            session.commit()
            print(f"✅ User updated: {user}")
            return user
        else:
            print(f"❌ User with id {user_id} not found")
            return None
    
    @staticmethod
    def delete_user(user_id):
        """Delete a user"""
        user = session.query(User).filter_by(id=user_id).first()
        if user:
            session.delete(user)
            session.commit()
            print(f"✅ User deleted: id={user_id}")
            return True
        else:
            print(f"❌ User with id {user_id} not found")
            return False
    
    @staticmethod
    def get_all_users():
        """Get all users"""
        users = session.query(User).all()
        print(f"\n📋 Total users: {len(users)}")
        for user in users:
            print(f"  {user}")
        return users
    
    # ⭐ EJERCICIO EXTRA 1
    @staticmethod
    def get_users_with_multiple_automobiles():
        """Get all users that have more than 1 automobile"""
        users = session.query(User).join(User.automobiles).group_by(User.id).having(func.count(Automobile.id) > 1).all()
        print(f"\n👥 Users with more than 1 automobile: {len(users)}")
        for user in users:
            print(f"  {user} - Automobiles: {len(user.automobiles)}")
        return users
    
    # ⭐ EJERCICIO EXTRA 2
    @staticmethod
    def print_user_details(user_id):
        """Print all automobiles and addresses of a user using relationships"""
        user = session.query(User).filter_by(id=user_id).first()
        
        if not user:
            print(f"❌ User with id {user_id} not found")
            return None
        
        print("\n" + "="*60)
        print(f"👤 USER DETAILS: {user.name} ({user.email})")
        print("="*60)
        
        # Usando la relación bidireccional: usuario.automobiles
        print(f"\n🚗 AUTOMOBILES ({len(user.automobiles)}):")
        if user.automobiles:
            for auto in user.automobiles:
                print(f"  - {auto.brand} {auto.model} ({auto.year})")
        else:
            print("  No automobiles associated")
        
        # Usando la relación bidireccional: usuario.addresses
        print(f"\n📍 ADDRESSES ({len(user.addresses)}):")
        if user.addresses:
            for addr in user.addresses:
                print(f"  - {addr.street}, {addr.city}")
        else:
            print("  No addresses associated")
        
        print("="*60)
        return user


class AutomobileOperations:
    """Class to manage automobile operations"""
    
    @staticmethod
    def create_automobile(brand, model, year, user_id=None):
        """Create a new automobile"""
        new_auto = Automobile(brand=brand, model=model, year=year, user_id=user_id)
        session.add(new_auto)
        session.commit()
        print(f"✅ Automobile created: {new_auto}")
        return new_auto
    
    @staticmethod
    def update_automobile(auto_id, brand=None, model=None, year=None, user_id=None):
        """Update an existing automobile"""
        auto = session.query(Automobile).filter_by(id=auto_id).first()
        if auto:
            if brand:
                auto.brand = brand
            if model:
                auto.model = model
            if year:
                auto.year = year
            if user_id is not None:
                auto.user_id = user_id
            session.commit()
            print(f"✅ Automobile updated: {auto}")
            return auto
        else:
            print(f"❌ Automobile with id {auto_id} not found")
            return None
    
    @staticmethod
    def delete_automobile(auto_id):
        """Delete an automobile"""
        auto = session.query(Automobile).filter_by(id=auto_id).first()
        if auto:
            session.delete(auto)
            session.commit()
            print(f"✅ Automobile deleted: id={auto_id}")
            return True
        else:
            print(f"❌ Automobile with id {auto_id} not found")
            return False
    
    @staticmethod
    def get_all_automobiles():
        """Get all automobiles"""
        autos = session.query(Automobile).all()
        print(f"\n🚗 Total automobiles: {len(autos)}")
        for auto in autos:
            print(f"  {auto}")
        return autos
    
    @staticmethod
    def assign_automobile_to_user(auto_id, user_id):
        """Assign an automobile to a user"""
        auto = session.query(Automobile).filter_by(id=auto_id).first()
        user = session.query(User).filter_by(id=user_id).first()
        
        if auto and user:
            auto.user_id = user_id
            session.commit()
            print(f"✅ Automobile {auto.brand} {auto.model} assigned to {user.name}")
            return True
        else:
            print(f"❌ Automobile or User not found")
            return False
    
    # ⭐ EJERCICIO EXTRA 1
    @staticmethod
    def get_automobiles_without_user():
        """Get all automobiles that don't have an associated user"""
        autos = session.query(Automobile).filter(Automobile.user_id == None).all()
        print(f"\n🚗 Automobiles without user: {len(autos)}")
        for auto in autos:
            print(f"  {auto}")
        return autos


class AddressOperations:
    """Class to manage address operations"""
    
    @staticmethod
    def create_address(street, city, user_id):
        """Create a new address"""
        new_address = Address(street=street, city=city, user_id=user_id)
        session.add(new_address)
        session.commit()
        print(f"✅ Address created: {new_address}")
        return new_address
    
    @staticmethod
    def update_address(address_id, street=None, city=None):
        """Update an existing address"""
        address = session.query(Address).filter_by(id=address_id).first()
        if address:
            if street:
                address.street = street
            if city:
                address.city = city
            session.commit()
            print(f"✅ Address updated: {address}")
            return address
        else:
            print(f"❌ Address with id {address_id} not found")
            return None
    
    @staticmethod
    def delete_address(address_id):
        """Delete an address"""
        address = session.query(Address).filter_by(id=address_id).first()
        if address:
            session.delete(address)
            session.commit()
            print(f"✅ Address deleted: id={address_id}")
            return True
        else:
            print(f"❌ Address with id {address_id} not found")
            return False
    
    @staticmethod
    def get_all_addresses():
        """Get all addresses"""
        addresses = session.query(Address).all()
        print(f"\n📍 Total addresses: {len(addresses)}")
        for addr in addresses:
            print(f"  {addr}")
        return addresses
    
    # ⭐ EJERCICIO EXTRA 1
    @staticmethod
    def get_addresses_with_calle():
        """Get all addresses that contain 'Calle' in their street name"""
        addresses = session.query(Address).filter(Address.street.like('%Calle%')).all()
        print(f"\n📍 Addresses containing 'Calle': {len(addresses)}")
        for addr in addresses:
            print(f"  {addr}")
        return addresses



if __name__ == "__main__":
    print("\n" + "="*60)
    print("🧪 TESTING OPERATIONS")
    print("="*60)
    
    # Create users
    user1 = UserOperations.create_user("Jeff Berrocal", "jeff@vlacademy.com")
    user2 = UserOperations.create_user("Maria Lopez", "maria@example.com")
    
    # Create addresses
    AddressOperations.create_address("Calle Principal 123", "San Jose", user1.id)
    AddressOperations.create_address("Avenida Central 456", "Alajuela", user1.id)
    
    # Create automobiles
    auto1 = AutomobileOperations.create_automobile("Toyota", "Corolla", 2020)
    auto2 = AutomobileOperations.create_automobile("Honda", "Civic", 2021)
    auto3 = AutomobileOperations.create_automobile("Mazda", "CX-5", 2022)
    
    # Assign automobiles
    AutomobileOperations.assign_automobile_to_user(auto1.id, user1.id)
    AutomobileOperations.assign_automobile_to_user(auto2.id, user1.id)
    
    # Query all
    UserOperations.get_all_users()
    AddressOperations.get_all_addresses()
    AutomobileOperations.get_all_automobiles()
    
    # ⭐ TESTING EJERCICIO EXTRA 1
    print("\n" + "="*60)
    print("🌟 TESTING ADVANCED FILTERS (Extra 1)")
    print("="*60)
    
    AutomobileOperations.get_automobiles_without_user()
    UserOperations.get_users_with_multiple_automobiles()
    AddressOperations.get_addresses_with_calle()
    
    # ⭐ TESTING EJERCICIO EXTRA 2
    print("\n" + "="*60)
    print("🌟 TESTING BIDIRECTIONAL RELATIONSHIPS (Extra 2)")
    print("="*60)
    
    UserOperations.print_user_details(user1.id)
    UserOperations.print_user_details(user2.id)
    
    print("\n✅ All operations completed successfully!")