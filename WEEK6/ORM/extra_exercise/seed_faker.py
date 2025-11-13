"""
Seed script using Faker to generate fake data
Ejercicio Extra 3: Seed inicial con datos falsos usando Faker
"""

from faker import Faker
import random
from operations import UserOperations, AddressOperations, AutomobileOperations

# Initialize Faker with Spanish locale
fake = Faker('es_ES')

# Car brands and models for realistic data
CAR_DATA = {
    'Toyota': ['Corolla', 'Camry', 'RAV4', 'Yaris', 'Hilux'],
    'Honda': ['Civic', 'Accord', 'CR-V', 'Fit', 'HR-V'],
    'Mazda': ['Mazda3', 'CX-5', 'CX-30', 'Mazda6', 'MX-5'],
    'Ford': ['Focus', 'Fiesta', 'Explorer', 'Mustang', 'Ranger'],
    'Chevrolet': ['Spark', 'Cruze', 'Malibu', 'Equinox', 'Silverado'],
    'Nissan': ['Sentra', 'Versa', 'Altima', 'Rogue', 'Frontier'],
    'Hyundai': ['Elantra', 'Accent', 'Tucson', 'Santa Fe', 'Kona'],
    'Kia': ['Rio', 'Forte', 'Sportage', 'Sorento', 'Soul'],
}


def generate_users(num_users=20):
    """Generate fake users"""
    print("\n" + "="*60)
    print(f"🎭 GENERATING {num_users} FAKE USERS")
    print("="*60)
    
    users = []
    for i in range(num_users):
        name = fake.name()
        email = fake.email()
        
        try:
            user = UserOperations.create_user(name, email)
            users.append(user)
        except Exception as e:
            print(f"⚠️  Error creating user {name}: {e}")
    
    print(f"\n✅ Created {len(users)} users")
    return users


def generate_addresses(users):
    """Generate fake addresses for users"""
    print("\n" + "="*60)
    print(f"🏠 GENERATING ADDRESSES FOR USERS")
    print("="*60)
    
    addresses = []
    for user in users:
        # Each user gets 1-3 addresses
        num_addresses = random.randint(1, 3)
        
        for _ in range(num_addresses):
            street = fake.street_address()
            city = fake.city()
            
            try:
                address = AddressOperations.create_address(street, city, user.id)
                addresses.append(address)
            except Exception as e:
                print(f"⚠️  Error creating address for user {user.name}: {e}")
    
    print(f"\n✅ Created {len(addresses)} addresses")
    return addresses


def generate_automobiles(users, num_automobiles=30):
    """Generate fake automobiles, some assigned to users, some without user"""
    print("\n" + "="*60)
    print(f"🚗 GENERATING {num_automobiles} AUTOMOBILES")
    print("="*60)
    
    automobiles = []
    
    for i in range(num_automobiles):
        # Random brand and model
        brand = random.choice(list(CAR_DATA.keys()))
        model = random.choice(CAR_DATA[brand])
        year = random.randint(2015, 2024)
        
        # 70% of cars will have a user, 30% will be unassigned
        if random.random() < 0.7 and users:
            user = random.choice(users)
            user_id = user.id
        else:
            user_id = None
        
        try:
            auto = AutomobileOperations.create_automobile(brand, model, year, user_id)
            automobiles.append(auto)
        except Exception as e:
            print(f"⚠️  Error creating automobile {brand} {model}: {e}")
    
    print(f"\n✅ Created {len(automobiles)} automobiles")
    
    # Count assigned vs unassigned
    assigned = sum(1 for auto in automobiles if auto.user_id is not None)
    unassigned = len(automobiles) - assigned
    print(f"   📊 {assigned} assigned to users")
    print(f"   📊 {unassigned} without user")
    
    return automobiles


def seed_database(num_users=20, num_automobiles=30):
    """Main function to seed the database"""
    print("\n" + "="*70)
    print("🌱 STARTING DATABASE SEEDING WITH FAKER")
    print("="*70)
    
    # Generate users
    users = generate_users(num_users)
    
    # Generate addresses for users
    addresses = generate_addresses(users)
    
    # Generate automobiles (some with users, some without)
    automobiles = generate_automobiles(users, num_automobiles)
    
    # Summary
    print("\n" + "="*70)
    print("📊 SEEDING SUMMARY")
    print("="*70)
    print(f"👥 Total users created: {len(users)}")
    print(f"🏠 Total addresses created: {len(addresses)}")
    print(f"🚗 Total automobiles created: {len(automobiles)}")
    print("="*70)
    
    return users, addresses, automobiles


if __name__ == "__main__":
    # Run the seed
    users, addresses, automobiles = seed_database(num_users=20, num_automobiles=30)
    
    print("\n✅ Database seeding completed successfully!")
    print("\n💡 You can now run operations.py to test the data")