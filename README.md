# Proyecto Tienda - Pet Shop API

API REST para la gestión de una tienda de mascotas desarrollada con Flask.

## Requisitos

- Python 3.7 o superior
- pip (gestor de paquetes de Python)

## Instalación

1. Clonar el repositorio o descargar el proyecto

2. Instalar las dependencias necesarias:
```bash
pip install flask
```

## Ejecución

Para ejecutar el proyecto:

```bash
python main.py
```

La aplicación se ejecutará en modo debug en `http://127.0.0.1:5000`

## Endpoints Disponibles

### Autenticación

- **POST** `/register` - Registro de usuarios (stub)
- **POST** `/login` - Inicio de sesión (stub)

### Usuarios

- **GET** `/users` - Obtener todos los usuarios
- **POST** `/users` - Crear un nuevo usuario
  - Body: `{"name": "string", "email": "string", "password": "string"}`
- **PUT** `/users/<id>` - Actualizar usuario por ID
  - Body: `{"name": "string", "email": "string", "password": "string"}`
- **DELETE** `/users/<id>` - Eliminar usuario por ID

### Productos

- **GET** `/products` - Obtener todos los productos
- **POST** `/products` - Crear un nuevo producto
  - Body: `{"name": "string", "price": float, "stock": int}`
- **PUT** `/products/<id>` - Actualizar producto por ID
  - Body: `{"name": "string", "price": float, "stock": int}`
- **DELETE** `/products/<id>` - Eliminar producto por ID

### Facturas

- **GET** `/bills` - Obtener todas las facturas
- **POST** `/bills` - Crear una nueva factura
  - Body: `{"user_id": int, "products": [], "total": float}`
- **PUT** `/bills/<id>` - Actualizar factura por ID
  - Body: `{"user_id": int, "products": [], "total": float}`
- **DELETE** `/bills/<id>` - Eliminar factura por ID

## Estructura del Proyecto

```
ProyectoTienda/
├── main.py              # Punto de entrada de la aplicación
├── auth.py              # Módulo de autenticación
├── users.py             # Gestión de usuarios
├── products.py          # Gestión de productos
├── bill.py              # Gestión de facturas
├── json_hadler.py       # Utilidad para manejo de archivos JSON
└── data/
    ├── users.json       # Almacenamiento de usuarios
    ├── products.json    # Almacenamiento de productos
    └── bills.json       # Almacenamiento de facturas
```

## Persistencia de Datos

La aplicación utiliza archivos JSON para la persistencia de datos, ubicados en el directorio `data/`:

- `users.json` - Almacena los usuarios registrados
- `products.json` - Almacena el catálogo de productos
- `bills.json` - Almacena las facturas generadas

## Ejemplos de Uso con cURL

### Crear un usuario
```bash
curl -X POST http://127.0.0.1:5000/users \
  -H "Content-Type: application/json" \
  -d '{"name":"Maria","email":"maria@correo.com","password":"12345"}'
```

### Obtener todos los productos
```bash
curl http://127.0.0.1:5000/products
```

### Crear un producto
```bash
curl -X POST http://127.0.0.1:5000/products \
  -H "Content-Type: application/json" \
  -d '{"name":"Juguete para gatos","price":12.99,"stock":25}'
```

### Crear una factura
```bash
curl -X POST http://127.0.0.1:5000/bills \
  -H "Content-Type: application/json" \
  -d '{"user_id":1,"products":[{"product_id":1,"name":"Alimento para perros","quantity":1,"price":25.99}],"total":25.99}'
```

## Notas

- La aplicación se ejecuta en modo debug, adecuado solo para desarrollo
- Los IDs se generan automáticamente de forma incremental
- Para producción, se recomienda usar una base de datos real en lugar de archivos JSON
