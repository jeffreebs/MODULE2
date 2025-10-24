import psycopg2
from datetime import datetime, timedelta
import random

try:
    # Connect
    conexion = psycopg2.connect(
        host="localhost",
        database="postgres",
        user="postgres",
        password="1MillionDollar",
        port="5432"
    )
    
    cursor = conexion.cursor()
    
    
    create_table = """
    CREATE TABLE IF NOT EXISTS lyfter_car_rental.rentals (
        id SERIAL PRIMARY KEY,
        user_id INTEGER NOT NULL,
        car_id INTEGER NOT NULL,
        rental_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        return_date TIMESTAMP,
        rental_status VARCHAR(20) DEFAULT 'active',
        FOREIGN KEY (user_id) REFERENCES lyfter_car_rental.users(id),
        FOREIGN KEY (car_id) REFERENCES lyfter_car_rental.cars(id)
    );
    """
    
    cursor.execute(create_table)
    print("✅ 'rentals' Table created successfully!")
    
    
    cursor.execute("SELECT id FROM lyfter_car_rental.users;")
    user_ids = [row[0] for row in cursor.fetchall()]
    
    
    cursor.execute("SELECT id FROM lyfter_car_rental.cars;")
    car_ids = [row[0] for row in cursor.fetchall()]
    
    print(f"📊 Found {len(user_ids)} users and {len(car_ids)} cars")
    
    
    insert_rental = """
    INSERT INTO lyfter_car_rental.rentals 
    (user_id, car_id, rental_date, return_date, rental_status)
    VALUES (%s, %s, %s, %s, %s);
    """
    
    statuses = ['active', 'completed', 'cancelled']
    
    print("📝 Creating rental records...")
    
    
    num_rentals = random.randint(20, 30)
    used_cars = set()  # Para evitar alquilar el mismo auto dos veces activamente
    
    for i in range(num_rentals):
        user_id = random.choice(user_ids)
        
        
        available_cars = [c for c in car_ids if c not in used_cars]
        if not available_cars:
            available_cars = car_ids  
        
        car_id = random.choice(available_cars)
        
        
        days_ago = random.randint(0, 90)
        rental_date = datetime.now() - timedelta(days=days_ago)
        
        
        status = random.choice(statuses)
        
        if status == 'completed':
            
            return_days = random.randint(1, 14)
            return_date = rental_date + timedelta(days=return_days)
        elif status == 'active':
            
            return_date = None
            used_cars.add(car_id)  
        else:  
            
            return_date = rental_date
        
        cursor.execute(insert_rental, (user_id, car_id, rental_date, return_date, status))
    
    print(f"✅ {num_rentals} rental records created successfully!")
    
    
    conexion.commit()
    
    
    cursor.execute("SELECT COUNT(*) FROM Lyfter_car_rental.rentals;")
    total = cursor.fetchone()[0]
    print(f"📊 Total rentals in table: {total}")
    
    
    cursor.execute("""
        SELECT rental_status, COUNT(*) 
        FROM lyfter_car_rental.rentals 
        GROUP BY rental_status;
    """)
    status_counts = cursor.fetchall()
    
    print("\n📈 Rentals by status:")
    for status, count in status_counts:
        print(f"  {status}: {count}")
    
    
    cursor.execute("""
        SELECT r.id, u.name, u.username, c.brand, c.model, r.rental_date, r.rental_status
        FROM lyfter_car_rental.rentals r
        JOIN lyfter_car_rental.users u ON r.user_id = u.id
        JOIN lyfter_car_rental.cars c ON r.car_id = c.id
        LIMIT 5;
    """)
    examples = cursor.fetchall()
    
    print("\n🚗 Example Rentals:")
    for rental in examples:
        print(f"  ID: {rental[0]} | User: {rental[1]} ({rental[2]}) | Car: {rental[3]} {rental[4]} | Date: {rental[5].strftime('%Y-%m-%d')} | Status: {rental[6]}")
    
    cursor.close()
    conexion.close()
    
    print("\n🎉 ALL TABLES COMPLETED! Database is ready to use!")
    
except Exception as error:
    print(f"❌ Error: {error}")
    if 'conexion' in locals():
        conexion.rollback()