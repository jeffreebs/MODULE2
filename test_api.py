import unittest
import json
from main import app
from database import get_connection, engine
from models import users_table, products_table, roles_table, user_roles_table, carts_table, cart_items_table
from sqlalchemy import insert, delete, select
import hashlib

class TestPetShopAPI(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        """Configuración inicial antes de todos los tests"""
        cls.client = app.test_client()
        cls.client.testing = True
        
    def setUp(self):
        """Configuración antes de cada test"""
        
        self.test_user_email = "test@test.com"
        self.test_admin_email = "admin@test.com"
        self.test_password = "testpass123"
        
        conn = get_connection()
        
        
        conn.execute(delete(user_roles_table).where(
            user_roles_table.c.user_id.in_(
                [1000, 1001]
            )
        ))
        conn.execute(delete(users_table).where(
            users_table.c.email.in_([self.test_user_email, self.test_admin_email])
        ))
        conn.commit()
        
        
        hashed_password = hashlib.sha256(self.test_password.encode()).hexdigest()
        stmt = insert(users_table).values(
            id=1000,
            name="Test User",
            email=self.test_user_email,
            password=hashed_password
        )
        conn.execute(stmt)
        
        
        stmt = insert(user_roles_table).values(user_id=1000, role_id=2)
        conn.execute(stmt)
        
        
        stmt = insert(users_table).values(
            id=1001,
            name="Test Admin",
            email=self.test_admin_email,
            password=hashed_password
        )
        conn.execute(stmt)
        
        
        stmt = insert(user_roles_table).values(user_id=1001, role_id=1)
        conn.execute(stmt)
        
        conn.commit()
        conn.close()
    
    def tearDown(self):
        """Limpieza después de cada test"""
        conn = get_connection()
        conn.execute(delete(user_roles_table).where(
            user_roles_table.c.user_id.in_([1000, 1001])
        ))
        conn.execute(delete(users_table).where(
            users_table.c.email.in_([self.test_user_email, self.test_admin_email])
        ))
        conn.commit()
        conn.close()


class TestAuthEndpoints(TestPetShopAPI):
    """Tests para endpoints de autenticación"""
    
    def test_register_success(self):
        """Test: Registro exitoso de nuevo usuario"""
        
        conn = get_connection()
        try:
            stmt_user = select(users_table.c.id).where(users_table.c.email == "newuser@test.com")
            user_result = conn.execute(stmt_user).fetchone()
            
            if user_result:
                user_id = user_result[0]
                conn.execute(delete(user_roles_table).where(user_roles_table.c.user_id == user_id))
                conn.execute(delete(users_table).where(users_table.c.id == user_id))
                conn.commit()
        except:
            conn.rollback()
        finally:
            conn.close()
        
        
        data = {
            "name": "New User",
            "email": "newuser@test.com",
            "password": "password123"
        }
        response = self.client.post('/register', 
                                    data=json.dumps(data),
                                    content_type='application/json')
        
        self.assertEqual(response.status_code, 201)
        response_data = json.loads(response.data)
        self.assertEqual(response_data["message"], "Successfully registered")
        
        
        conn = get_connection()
        try:
            stmt_user = select(users_table.c.id).where(users_table.c.email == "newuser@test.com")
            user_result = conn.execute(stmt_user).fetchone()
            
            if user_result:
                user_id = user_result[0]
                conn.execute(delete(user_roles_table).where(user_roles_table.c.user_id == user_id))
                conn.execute(delete(users_table).where(users_table.c.id == user_id))
                conn.commit()
        except Exception as e:
            print(f"Error en limpieza: {e}")
            conn.rollback()
        finally:
            conn.close()
    
    def test_register_missing_fields(self):
        """Test: Registro con campos faltantes debe fallar"""
        data = {
            "name": "New User",
            "email": "incomplete@test.com"
            
        }
        response = self.client.post('/register',
                                    data=json.dumps(data),
                                    content_type='application/json')
        
        
        self.assertIn(response.status_code, [400, 500])
    
    def test_login_success(self):
        """Test: Login exitoso con credenciales correctas"""
        data = {
            "email": self.test_user_email,
            "password": self.test_password
        }
        response = self.client.post('/login',
                                    data=json.dumps(data),
                                    content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertEqual(response_data["message"], "Successfully login")
        self.assertIn("user_id", response_data)
    
    def test_login_invalid_credentials(self):
        """Test: Login con credenciales incorrectas debe fallar"""
        data = {
            "email": self.test_user_email,
            "password": "wrongpassword"
        }
        response = self.client.post('/login',
                                    data=json.dumps(data),
                                    content_type='application/json')
        
        self.assertEqual(response.status_code, 401)
        response_data = json.loads(response.data)
        self.assertEqual(response_data["error"], "Invalid credentials")
    
    def test_login_nonexistent_user(self):
        """Test: Login con usuario inexistente debe fallar"""
        data = {
            "email": "nonexistent@test.com",
            "password": "password123"
        }
        response = self.client.post('/login',
                                    data=json.dumps(data),
                                    content_type='application/json')
        
        self.assertEqual(response.status_code, 401)
        response_data = json.loads(response.data)
        self.assertEqual(response_data["error"], "Invalid credentials")


class TestProductEndpoints(TestPetShopAPI):
    """Tests para endpoints de productos"""
    
    def test_get_products_success(self):
        """Test: Obtener lista de productos exitosamente"""
        response = self.client.get('/products')
        
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        # Debe tener source y data
        self.assertIn("source", response_data)
        self.assertIn("data", response_data)
        self.assertIsInstance(response_data["data"], list)
    
    def test_get_product_by_id_success(self):
        """Test: Obtener producto por ID exitosamente"""
        # Asumiendo que existe un producto con id=1
        response = self.client.get('/products/1')
        
        if response.status_code == 200:
            response_data = json.loads(response.data)
            self.assertIn("source", response_data)
            self.assertIn("data", response_data)
            self.assertIsInstance(response_data["data"], dict)
    
    def test_get_product_not_found(self):
        """Test: Obtener producto inexistente debe retornar 404"""
        response = self.client.get('/products/99999')
        
        self.assertEqual(response.status_code, 404)
        response_data = json.loads(response.data)
        self.assertEqual(response_data["error"], "Product not found")
    
    def test_create_product_without_auth(self):
        """Test: Crear producto sin autenticación debe fallar"""
        data = {
            "sku": "TEST-001",
            "name": "Test Product",
            "price": 10.99,
            "stock": 100
        }
        response = self.client.post('/products',
                                    data=json.dumps(data),
                                    content_type='application/json')
        
        self.assertEqual(response.status_code, 401)
        response_data = json.loads(response.data)
        self.assertEqual(response_data["error"], "User ID required")
    
    def test_create_product_as_cliente(self):
        """Test: Crear producto como cliente debe fallar (requiere admin)"""
        data = {
            "sku": "TEST-002",
            "name": "Test Product",
            "price": 10.99,
            "stock": 100
        }
        response = self.client.post('/products',
                                    data=json.dumps(data),
                                    content_type='application/json',
                                    headers={'user_id': '1000'})  # Cliente
        
        self.assertEqual(response.status_code, 403)
        response_data = json.loads(response.data)
        self.assertIn("Access denied", response_data["error"])
    
    def test_create_product_as_admin_success(self):
        """Test: Crear producto como admin exitosamente"""
        data = {
            "sku": "TEST-003",
            "name": "Test Product Admin",
            "price": 15.99,
            "stock": 50,
            "category": "Test Category"
        }
        response = self.client.post('/products',
                                    data=json.dumps(data),
                                    content_type='application/json',
                                    headers={'user_id': '1001'})  # Admin
        
        self.assertEqual(response.status_code, 201)
        response_data = json.loads(response.data)
        self.assertEqual(response_data["message"], "Product created")
        
        
        conn = get_connection()
        conn.execute(delete(products_table).where(products_table.c.sku == "TEST-003"))
        conn.commit()
        conn.close()
    
    def test_update_product_as_admin_success(self):
        """Test: Actualizar producto como admin exitosamente"""
        
        conn = get_connection()
        stmt = insert(products_table).values(
            sku="TEST-UPDATE",
            name="Original Name",
            price=10.00,
            stock=10
        ).returning(products_table.c.id)
        result = conn.execute(stmt)
        product_id = result.fetchone()[0]
        conn.commit()
        conn.close()
        
        data = {"name": "Updated Name", "price": 20.00}
        response = self.client.put(f'/products/{product_id}',
                                   data=json.dumps(data),
                                   content_type='application/json',
                                   headers={'user_id': '1001'})
        
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertEqual(response_data["message"], "Product updated")
        
        
        conn = get_connection()
        conn.execute(delete(products_table).where(products_table.c.id == product_id))
        conn.commit()
        conn.close()
    
    def test_update_nonexistent_product(self):
        """Test: Actualizar producto inexistente debe retornar 404"""
        data = {"name": "Updated Name"}
        response = self.client.put('/products/99999',
                                   data=json.dumps(data),
                                   content_type='application/json',
                                   headers={'user_id': '1001'})
        
        self.assertEqual(response.status_code, 404)
        response_data = json.loads(response.data)
        self.assertEqual(response_data["error"], "Product not found")
    
    def test_delete_product_as_admin_success(self):
        """Test: Eliminar producto como admin exitosamente"""
        
        conn = get_connection()
        stmt = insert(products_table).values(
            sku="TEST-DELETE",
            name="To Delete",
            price=10.00,
            stock=10
        ).returning(products_table.c.id)
        result = conn.execute(stmt)
        product_id = result.fetchone()[0]
        conn.commit()
        conn.close()
        
        
        response = self.client.delete(f'/products/{product_id}',
                                      headers={'user_id': '1001'})
        
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertEqual(response_data["message"], "Product deleted")


class TestUserEndpoints(TestPetShopAPI):
    """Tests para endpoints de usuarios"""
    
    def test_get_users_as_admin_success(self):
        """Test: Admin puede obtener lista de usuarios"""
        response = self.client.get('/users',
                                   headers={'user_id': '1001'})
        
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertIn("source", response_data)
        self.assertIn("data", response_data)
        self.assertIsInstance(response_data["data"], list)
    
    def test_get_users_as_cliente_fails(self):
        """Test: Cliente no puede obtener lista de usuarios"""
        response = self.client.get('/users',
                                   headers={'user_id': '1000'})
        
        self.assertEqual(response.status_code, 403)
        response_data = json.loads(response.data)
        self.assertIn("Access denied", response_data["error"])
    
    def test_get_users_without_auth(self):
        """Test: Sin autenticación no puede obtener usuarios"""
        response = self.client.get('/users')
        
        self.assertIn(response.status_code, [401, 415])


class TestCartEndpoints(TestPetShopAPI):
    """Tests para endpoints de carritos"""
    
    def test_create_cart_success(self):
        """Test: Crear carrito exitosamente"""
        data = {"user_id": 1000}
        response = self.client.post('/carts',
                                    data=json.dumps(data),
                                    content_type='application/json',
                                    headers={'user_id': '1000'})
        
        if response.status_code == 201:
            response_data = json.loads(response.data)
            self.assertEqual(response_data["message"], "Cart created")
            self.assertIn("cart_id", response_data)
            
            
            cart_id = response_data["cart_id"]
            conn = get_connection()
            conn.execute(delete(carts_table).where(carts_table.c.id == cart_id))
            conn.commit()
            conn.close()
    
    def test_get_cart_not_found(self):
        """Test: Obtener carrito inexistente debe retornar 404"""
        response = self.client.get('/carts/99999')
        
        self.assertEqual(response.status_code, 404)
        response_data = json.loads(response.data)
        self.assertEqual(response_data["error"], "Cart not found")


class TestBillEndpoints(TestPetShopAPI):
    """Tests para endpoints de facturas"""
    
    def test_get_all_bills_as_admin_success(self):
        """Test: Admin puede obtener todas las facturas"""
        response = self.client.get('/bills',
                                   headers={'user_id': '1001'})
        
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertIn("source", response_data)
        self.assertIn("data", response_data)
        self.assertIsInstance(response_data["data"], list)
    
    def test_get_all_bills_as_cliente_fails(self):
        """Test: Cliente no puede obtener todas las facturas"""
        response = self.client.get('/bills',
                                   headers={'user_id': '1000'})
        
        self.assertEqual(response.status_code, 403)
        response_data = json.loads(response.data)
        self.assertIn("Access denied", response_data["error"])
    
    def test_get_user_bills_access_denied(self):
        """Test: Usuario no puede ver facturas de otro usuario"""
        response = self.client.get('/bills/user/999',
                                   headers={'user_id': '1000'})
        
        self.assertEqual(response.status_code, 403)
        response_data = json.loads(response.data)
        self.assertEqual(response_data["error"], "Access denied")
    
    def test_get_bill_not_found(self):
        """Test: Obtener factura inexistente debe retornar 404"""
        response = self.client.get('/bills/99999',
                                   headers={'user_id': '1001'})
        
        self.assertEqual(response.status_code, 404)
        response_data = json.loads(response.data)
        self.assertEqual(response_data["error"], "Bill not found")


if __name__ == '__main__':
    
    unittest.main(verbosity=2)