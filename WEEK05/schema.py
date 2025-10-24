import psycopg2

try: 
    conection = psycopg2.connect (
            host="localhost",
        database="postgres",
        user="postgres",
        password="1MillionDollar",  # ⚠️ Cambia esto
        port="5432"
    )


    conection.autocommit = True
    cursor = conection.cursor ()

    cursor.execute("CREATE SCHEMA IF NOT EXISTS Lyfter_car_rental;")
    print("✅ Schema 'Lyfter_car_rental' created successfully!")


    cursor.close()
    conection.close()


except Exception  as error:
    print (f"Error : {error}")