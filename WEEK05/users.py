import psycopg2
from faker import Faker
import random

fake = Faker('en')  

try:
    conexion = psycopg2.connect(
        host="localhost",
        database="postgres",
        user="postgres",
        password="1MillionDollar",
        port="5432"
    )
    
    cursor = conexion.cursor()
    
    
    crear_tabla = """
    CREATE TABLE IF NOT EXISTS lyfter_car_rental.users (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL,
        username VARCHAR(50) UNIQUE NOT NULL,
        password VARCHAR(100) NOT NULL,
        birth_date DATE NOT NULL,
        account_status VARCHAR(20) DEFAULT 'active'
    );
    """
    
    cursor.execute(crear_tabla)
    print("✅ 'users' Table created successfully!")
    
    
    insert_user = """
    INSERT INTO lyfter_car_rental.users 
    (name, email, username, password, birth_date, account_status)
    VALUES (%s, %s, %s, %s, %s, %s);
    """
    
    statuses = ['active', 'inactive', 'suspended']
    
    print("📝 Inserting 50 users...")
    
    for i in range(50):
        name = fake.name()
        email = fake.email()
        username = fake.user_name() + str(i)
        password = fake.password()
        birth_date = fake.date_of_birth(minimum_age=18, maximum_age=80)
        status = random.choice(statuses)
        
        cursor.execute(insert_user, (name, email, username, password, birth_date, status))
    
    print("✅ 50 users inserted successfully!")
    
    conexion.commit()
    
    
    cursor.execute("SELECT COUNT(*) FROM lyfter_car_rental.users;")
    total = cursor.fetchone()[0]
    print(f"📊 Total users in table: {total}")
    
    
    cursor.execute("SELECT id, name, username, account_status FROM lyfter_car_rental.users LIMIT 5;")
    examples = cursor.fetchall()
    
    print("\n👥 Created Users:")
    for user in examples:
        print(f"  ID: {user[0]} | Name: {user[1]} | Username: {user[2]} | Status: {user[3]}")
    
    cursor.close()
    conexion.close()
    
except Exception as error:
    print(f"❌ Error: {error}")
    if 'conexion' in locals():
        conexion.rollback()