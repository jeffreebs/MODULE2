
DROP TABLE IF EXISTS bills CASCADE;
DROP TABLE IF EXISTS sales CASCADE;
DROP TABLE IF EXISTS cart_items CASCADE;
DROP TABLE IF EXISTS carts CASCADE;
DROP TABLE IF EXISTS products CASCADE;
DROP TABLE IF EXISTS user_roles CASCADE;
DROP TABLE IF EXISTS roles CASCADE;
DROP TABLE IF EXISTS users CASCADE;

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE INDEX idx_users_email ON users(email);


COMMENT ON TABLE users IS 'Usuarios del sistema';
COMMENT ON COLUMN users.email IS 'Email único del usuario';


CREATE TABLE roles (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    description VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE INDEX idx_roles_name ON roles(name);

COMMENT ON TABLE roles IS 'Roles disponibles en el sistema (admin, cliente, vendedor)';


CREATE TABLE user_roles (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    role_id INT NOT NULL,
    assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,


    CONSTRAINT fk_user_roles_user FOREIGN KEY (user_id)
        REFERENCES users(id) ON DELETE CASCADE,
    CONSTRAINT fk_user_roles_role FOREIGN KEY (role_id)
        REFERENCES roles(id) ON DELETE CASCADE,

    
    CONSTRAINT unique_user_role UNIQUE (user_id, role_id)
);


CREATE INDEX idx_user_roles_user ON user_roles(user_id);
CREATE INDEX idx_user_roles_role ON user_roles(role_id);

COMMENT ON TABLE user_roles IS 'Asignación de roles a usuarios (relación N:M)';


CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    sku VARCHAR(50) NOT NULL UNIQUE,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    price DECIMAL(10,2) NOT NULL CHECK (price > 0),
    stock INT NOT NULL DEFAULT 0 CHECK (stock >= 0),
    category VARCHAR(100),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE INDEX idx_products_sku ON products(sku);
CREATE INDEX idx_products_category ON products(category);
CREATE INDEX idx_products_active ON products(is_active);

COMMENT ON TABLE products IS 'Catálogo de productos de la tienda';
COMMENT ON COLUMN products.sku IS 'Código único del producto (Stock Keeping Unit)';
COMMENT ON COLUMN products.is_active IS 'Indica si el producto está disponible para venta';


CREATE TABLE carts (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'active'
        CHECK (status IN ('active', 'completed', 'abandoned')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,

    
    CONSTRAINT fk_carts_user FOREIGN KEY (user_id)
        REFERENCES users(id) ON DELETE CASCADE
);


CREATE INDEX idx_carts_user_status ON carts(user_id, status);


CREATE UNIQUE INDEX idx_carts_user_active ON carts(user_id)
    WHERE status = 'active';

COMMENT ON TABLE carts IS 'Carritos de compra de los usuarios';
COMMENT ON COLUMN carts.status IS 'Estado del carrito: active, completed, abandoned';


CREATE TABLE cart_items (
    id SERIAL PRIMARY KEY,
    cart_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL DEFAULT 1 CHECK (quantity > 0),
    price_at_addition DECIMAL(10,2) NOT NULL,
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    
    CONSTRAINT fk_cart_items_cart FOREIGN KEY (cart_id)
        REFERENCES carts(id) ON DELETE CASCADE,
    CONSTRAINT fk_cart_items_product FOREIGN KEY (product_id)
        REFERENCES products(id) ON DELETE RESTRICT,

    
    CONSTRAINT unique_cart_product UNIQUE (cart_id, product_id)
);


CREATE INDEX idx_cart_items_cart ON cart_items(cart_id);
CREATE INDEX idx_cart_items_product ON cart_items(product_id);

COMMENT ON TABLE cart_items IS 'Items (productos) dentro de cada carrito';
COMMENT ON COLUMN cart_items.price_at_addition IS 'Precio del producto al momento de agregarlo al carrito';


CREATE TABLE sales (
    id SERIAL PRIMARY KEY,
    cart_id INT NOT NULL UNIQUE,
    user_id INT NOT NULL,
    total DECIMAL(10,2) NOT NULL CHECK (total >= 0),
    subtotal DECIMAL(10,2) NOT NULL CHECK (subtotal >= 0),
    tax DECIMAL(10,2) NOT NULL DEFAULT 0 CHECK (tax >= 0),
    payment_method VARCHAR(50) NOT NULL,
    sale_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    notes TEXT,

    
    CONSTRAINT fk_sales_cart FOREIGN KEY (cart_id)
        REFERENCES carts(id) ON DELETE RESTRICT,
    CONSTRAINT fk_sales_user FOREIGN KEY (user_id)
        REFERENCES users(id) ON DELETE RESTRICT,

    
    CONSTRAINT check_sales_total CHECK (total = subtotal + tax)
);


CREATE INDEX idx_sales_user ON sales(user_id);
CREATE INDEX idx_sales_date ON sales(sale_date);
CREATE INDEX idx_sales_cart ON sales(cart_id);

COMMENT ON TABLE sales IS 'Ventas realizadas en el sistema';
COMMENT ON COLUMN sales.cart_id IS 'Carrito que se convirtió en venta (relación 1:1)';


CREATE TABLE bills (
    id SERIAL PRIMARY KEY,
    sale_id INT NOT NULL UNIQUE,
    user_id INT NOT NULL,
    bill_number VARCHAR(50) NOT NULL UNIQUE,
    subtotal DECIMAL(10,2) NOT NULL CHECK (subtotal >= 0),
    tax DECIMAL(10,2) NOT NULL DEFAULT 0 CHECK (tax >= 0),
    total DECIMAL(10,2) NOT NULL CHECK (total >= 0),
    billing_name VARCHAR(200) NOT NULL,
    billing_address TEXT,
    billing_tax_id VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    
    CONSTRAINT fk_bills_sale FOREIGN KEY (sale_id)
        REFERENCES sales(id) ON DELETE RESTRICT,
    CONSTRAINT fk_bills_user FOREIGN KEY (user_id)
        REFERENCES users(id) ON DELETE RESTRICT,

    
    CONSTRAINT check_bills_total CHECK (total = subtotal + tax)
);


CREATE INDEX idx_bills_user ON bills(user_id);
CREATE INDEX idx_bills_sale ON bills(sale_id);
CREATE INDEX idx_bills_number ON bills(bill_number);

COMMENT ON TABLE bills IS 'Facturas generadas para las ventas';
COMMENT ON COLUMN bills.bill_number IS 'Número único de factura (formato: FAC-YYYY-XXXXX)';


CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER update_users_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();


CREATE TRIGGER update_products_updated_at
    BEFORE UPDATE ON products
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();


CREATE TRIGGER update_carts_updated_at
    BEFORE UPDATE ON carts
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();


DO $$
BEGIN
    RAISE NOTICE 'Schema de base de datos creado exitosamente!';
    RAISE NOTICE 'Tablas creadas: users, roles, user_roles, products, carts, cart_items, sales, bills';
END $$;
