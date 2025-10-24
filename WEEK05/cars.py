import psycopg2
from faker import Faker
import random

fake = Faker()

try:
    
    conexion = psycopg2.connect(
        host="localhost",
        database="postgres",
        user="postgres",
        password="1MillionDollar",
        port="5432"
    )
    
    cursor = conexion.cursor()
    
    
    create_table = """
    CREATE TABLE IF NOT EXISTS Lyfter_car_rental.cars (
        id SERIAL PRIMARY KEY,
        brand VARCHAR(50) NOT NULL,
        model VARCHAR(50) NOT NULL,
        year INTEGER NOT NULL,
        status VARCHAR(20) DEFAULT 'available'
    );
    """
    
    cursor.execute(create_table)
    print("✅ 'cars' Table created successfully!")
    
    
    brands_models = {
        'Toyota': ['Corolla', 'Camry', 'RAV4', 'Highlander', 'Prius'],
        'Honda': ['Civic', 'Accord', 'CR-V', 'Pilot', 'Fit'],
        'Ford': ['Mustang', 'F-150', 'Explorer', 'Escape', 'Focus'],
        'Chevrolet': ['Malibu', 'Silverado', 'Equinox', 'Tahoe', 'Cruze'],
        'Nissan': ['Altima', 'Sentra', 'Rogue', 'Pathfinder', 'Versa'],
        'Mazda': ['Mazda3', 'CX-5', 'Mazda6', 'CX-9', 'MX-5'],
        'Hyundai': ['Elantra', 'Tucson', 'Santa Fe', 'Sonata', 'Kona'],
        'Kia': ['Forte', 'Sportage', 'Sorento', 'Optima', 'Soul']
    }
    
    statuses = ['available', 'rented', 'maintenance', 'reserved']
    
    
    insert_car = """
    INSERT INTO Lyfter_car_rental.cars 
    (brand, model, year, status)
    VALUES (%s, %s, %s, %s);
    """
    
    print("📝 Inserting cars...")
    
    
    num_cars = random.randint(30, 40)
    
    for i in range(num_cars):
        brand = random.choice(list(brands_models.keys()))
        model = random.choice(brands_models[brand])
        year = random.randint(2015, 2024)
        status = random.choice(statuses)
        
        cursor.execute(insert_car, (brand, model, year, status))
    
    print(f"✅ {num_cars} cars inserted successfully!")
    
    
    conexion.commit()
    
    
    cursor.execute("SELECT COUNT(*) FROM Lyfter_car_rental.cars;")
    total = cursor.fetchone()[0]
    print(f"📊 Total cars in table: {total}")
    
    
    cursor.execute("SELECT id, brand, model, year, status FROM Lifter_car_rental.cars LIMIT 5;")
    examples = cursor.fetchall()
    
    print("\n🚗 Created Cars:")
    for car in examples:
        print(f"  ID: {car[0]} | {car[1]} {car[2]} ({car[3]}) | Status: {car[4]}")
    
    cursor.close()
    conexion.close()
    
except Exception as error:
    print(f"❌ Error: {error}")
    if 'conexion' in locals():
        conexion.rollback()