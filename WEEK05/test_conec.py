import psycopg2

try:
    # Conectar a PostgreSQL
    conexion = psycopg2.connect(
        host="localhost",
        database="postgres",  # Usa "postgres" que es la BD por defecto
        user="postgres",
        password="1MillionDollar",  # ⚠️ CAMBIA ESTO por tu contraseña
        port="5432"
    )
    
    print("✅ ¡Conexión exitosa a PostgreSQL!")
    
    # Crear un cursor para ejecutar consultas
    cursor = conexion.cursor()
    
    # Consulta de prueba: obtener la versión de PostgreSQL
    cursor.execute("SELECT version();")
    version = cursor.fetchone()
    print(f"📊 Versión de PostgreSQL: {version[0]}")
    
    # Cerrar cursor y conexión
    cursor.close()
    conexion.close()
    print("🔌 Conexión cerrada")
    
except Exception as error:
    print(f"❌ Error al conectar: {error}")