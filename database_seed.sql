INSERT INTO users (name, email, password) VALUES
('Juan Pérez', 'juan.perez@email.com', '$2b$10$hashed_password_1'),
('María González', 'maria.gonzalez@email.com', '$2b$10$hashed_password_2'),
('Carlos Rodríguez', 'carlos.rodriguez@email.com', '$2b$10$hashed_password_3'),
('Ana Martínez', 'ana.martinez@email.com', '$2b$10$hashed_password_4'),
('Luis Fernández', 'luis.fernandez@email.com', '$2b$10$hashed_password_5'),
('Sofia López', 'sofia.lopez@email.com', '$2b$10$hashed_password_6'),
('Diego Ramírez', 'diego.ramirez@email.com', '$2b$10$hashed_password_7'),
('Laura Torres', 'laura.torres@email.com', '$2b$10$hashed_password_8');


INSERT INTO roles (name, description) VALUES
('admin', 'Administrador del sistema con acceso completo'),
('cliente', 'Cliente que puede realizar compras'),
('vendedor', 'Empleado que gestiona ventas y productos');

-- ====================================
-- 3. ASIGNAR ROLES A USUARIOS
-- ====================================
INSERT INTO user_roles (user_id, role_id) VALUES
-- Juan es admin y vendedor
(1, 1),
(1, 3),
-- María es cliente
(2, 2),
-- Carlos es cliente
(3, 2),
-- Ana es vendedor
(4, 3),
-- Luis es cliente
(5, 2),
-- Sofia es cliente
(6, 2),
-- Diego es cliente
(7, 2),
-- Laura es admin
(8, 1);

-- ====================================
-- 4. INSERTAR PRODUCTOS
-- ====================================
INSERT INTO products (sku, name, description, price, stock, category, is_active) VALUES
-- Alimentos para perros
('DOG-FOOD-001', 'Alimento para perros adultos 15kg', 'Alimento premium para perros adultos de todas las razas', 45.99, 50, 'Alimento Perros', TRUE),
('DOG-FOOD-002', 'Alimento para cachorros 10kg', 'Nutrición completa para cachorros en crecimiento', 52.50, 35, 'Alimento Perros', TRUE),
('DOG-FOOD-003', 'Alimento para perros senior 12kg', 'Fórmula especial para perros mayores de 7 años', 48.75, 28, 'Alimento Perros', TRUE),

-- Alimentos para gatos
('CAT-FOOD-001', 'Alimento para gatos adultos 8kg', 'Alimento balanceado para gatos adultos', 38.99, 42, 'Alimento Gatos', TRUE),
('CAT-FOOD-002', 'Alimento para gatitos 5kg', 'Nutrición especial para gatitos de 2 a 12 meses', 35.50, 30, 'Alimento Gatos', TRUE),
('CAT-FOOD-003', 'Alimento húmedo para gatos (pack 12 latas)', 'Comida húmeda premium sabor pollo y pescado', 24.99, 60, 'Alimento Gatos', TRUE),

-- Accesorios para perros
('DOG-ACC-001', 'Collar ajustable para perros', 'Collar de nylon resistente, ajustable de 30-50cm', 8.99, 75, 'Accesorios Perros', TRUE),
('DOG-ACC-002', 'Correa retráctil 5 metros', 'Correa retráctil con freno de seguridad', 15.99, 45, 'Accesorios Perros', TRUE),
('DOG-ACC-003', 'Cama acolchada para perros grande', 'Cama ortopédica con funda lavable', 42.00, 22, 'Accesorios Perros', TRUE),
('DOG-ACC-004', 'Plato de acero inoxidable', 'Plato para comida y agua, antideslizante', 12.50, 55, 'Accesorios Perros', TRUE),

-- Accesorios para gatos
('CAT-ACC-001', 'Rascador de cartón', 'Rascador ecológico con catnip incluido', 18.99, 40, 'Accesorios Gatos', TRUE),
('CAT-ACC-002', 'Casa para gatos', 'Casa acogedora con cojín removible', 35.75, 18, 'Accesorios Gatos', TRUE),
('CAT-ACC-003', 'Arenero con tapa', 'Arenero cerrado para mayor privacidad', 28.50, 25, 'Accesorios Gatos', TRUE),
('CAT-ACC-004', 'Fuente de agua automática', 'Fuente con filtro para agua siempre fresca', 32.99, 15, 'Accesorios Gatos', TRUE),

-- Juguetes
('TOY-001', 'Pelota de tenis para perros (pack 3)', 'Pelotas resistentes para juego y ejercicio', 7.50, 80, 'Juguetes', TRUE),
('TOY-002', 'Juguete interactivo para gatos', 'Ratón automático con movimiento aleatorio', 22.99, 35, 'Juguetes', TRUE),
('TOY-003', 'Cuerda para jalar perros', 'Cuerda resistente de algodón natural', 9.99, 65, 'Juguetes', TRUE),
('TOY-004', 'Varita con plumas para gatos', 'Juguete interactivo con plumas naturales', 6.50, 70, 'Juguetes', TRUE),

-- Higiene y salud
('HEALTH-001', 'Champú para perros 500ml', 'Champú hipoalergénico con aroma fresco', 14.99, 50, 'Higiene', TRUE),
('HEALTH-002', 'Cepillo dental para mascotas', 'Kit de limpieza dental con pasta incluida', 11.50, 40, 'Higiene', TRUE),
('HEALTH-003', 'Pipeta antipulgas para perros', 'Protección por 30 días contra pulgas y garrapatas', 19.99, 8, 'Salud', TRUE),
('HEALTH-004', 'Vitaminas para gatos (60 tabletas)', 'Suplemento multivitamínico masticable', 16.75, 32, 'Salud', TRUE);

-- ====================================
-- 5. INSERTAR CARRITOS
-- ====================================

-- Carrito activo de María (user_id: 2)
INSERT INTO carts (user_id, status, created_at) VALUES
(2, 'active', CURRENT_TIMESTAMP - INTERVAL '2 hours');

-- Carrito completado de Carlos (user_id: 3)
INSERT INTO carts (user_id, status, created_at, completed_at) VALUES
(3, 'completed', CURRENT_TIMESTAMP - INTERVAL '5 days', CURRENT_TIMESTAMP - INTERVAL '5 days' + INTERVAL '30 minutes');

-- Carrito completado de Luis (user_id: 5)
INSERT INTO carts (user_id, status, created_at, completed_at) VALUES
(5, 'completed', CURRENT_TIMESTAMP - INTERVAL '3 days', CURRENT_TIMESTAMP - INTERVAL '3 days' + INTERVAL '15 minutes');

-- Carrito abandonado de Sofia (user_id: 6)
INSERT INTO carts (user_id, status, created_at) VALUES
(6, 'abandoned', CURRENT_TIMESTAMP - INTERVAL '10 days');

-- Carrito activo de Diego (user_id: 7)
INSERT INTO carts (user_id, status, created_at) VALUES
(7, 'active', CURRENT_TIMESTAMP - INTERVAL '1 hour');

-- Carrito completado de María (anterior)
INSERT INTO carts (user_id, status, created_at, completed_at) VALUES
(2, 'completed', CURRENT_TIMESTAMP - INTERVAL '15 days', CURRENT_TIMESTAMP - INTERVAL '15 days' + INTERVAL '20 minutes');

-- ====================================
-- 6. INSERTAR ITEMS EN CARRITOS
-- ====================================

-- Items en carrito activo de María (cart_id: 1)
INSERT INTO cart_items (cart_id, product_id, quantity, price_at_addition) VALUES
(1, 4, 2, 38.99),  -- 2 bolsas de alimento para gatos
(1, 15, 3, 7.50),  -- 3 packs de pelotas
(1, 11, 1, 18.99); -- 1 rascador

-- Items en carrito completado de Carlos (cart_id: 2)
INSERT INTO cart_items (cart_id, product_id, quantity, price_at_addition) VALUES
(2, 1, 1, 45.99),  -- 1 alimento para perros adultos
(2, 7, 1, 8.99),   -- 1 collar
(2, 8, 1, 15.99),  -- 1 correa
(2, 10, 2, 12.50); -- 2 platos

-- Items en carrito completado de Luis (cart_id: 3)
INSERT INTO cart_items (cart_id, product_id, quantity, price_at_addition) VALUES
(3, 2, 1, 52.50),  -- 1 alimento para cachorros
(3, 9, 1, 42.00),  -- 1 cama para perros
(3, 17, 1, 9.99),  -- 1 cuerda para jalar
(3, 19, 1, 14.99); -- 1 champú

-- Items en carrito abandonado de Sofia (cart_id: 4)
INSERT INTO cart_items (cart_id, product_id, quantity, price_at_addition) VALUES
(4, 6, 1, 24.99),  -- 1 pack de comida húmeda
(4, 18, 1, 6.50);  -- 1 varita con plumas

-- Items en carrito activo de Diego (cart_id: 5)
INSERT INTO cart_items (cart_id, product_id, quantity, price_at_addition) VALUES
(5, 12, 1, 35.75), -- 1 casa para gatos
(5, 14, 1, 32.99), -- 1 fuente de agua
(5, 22, 2, 16.75); -- 2 vitaminas para gatos

-- Items en carrito completado anterior de María (cart_id: 6)
INSERT INTO cart_items (cart_id, product_id, quantity, price_at_addition) VALUES
(6, 5, 1, 35.50),  -- 1 alimento para gatitos
(6, 13, 1, 28.50), -- 1 arenero
(6, 16, 1, 22.99); -- 1 juguete interactivo

-- ====================================
-- 7. INSERTAR VENTAS
-- ====================================

-- Venta de Carlos (cart_id: 2)
INSERT INTO sales (cart_id, user_id, subtotal, tax, total, payment_method, sale_date) VALUES
(2, 3, 95.97, 15.36, 111.33, 'tarjeta', CURRENT_TIMESTAMP - INTERVAL '5 days');

-- Venta de Luis (cart_id: 3)
INSERT INTO sales (cart_id, user_id, subtotal, tax, total, payment_method, sale_date) VALUES
(3, 5, 119.48, 19.12, 138.60, 'efectivo', CURRENT_TIMESTAMP - INTERVAL '3 days');

-- Venta de María anterior (cart_id: 6)
INSERT INTO sales (cart_id, user_id, subtotal, tax, total, payment_method, sale_date) VALUES
(6, 2, 86.99, 13.92, 100.91, 'transferencia', CURRENT_TIMESTAMP - INTERVAL '15 days');

-- ====================================
-- 8. INSERTAR FACTURAS
-- ====================================

-- Factura para venta de Carlos (sale_id: 1)
INSERT INTO bills (sale_id, user_id, bill_number, subtotal, tax, total, billing_name, billing_address, billing_tax_id) VALUES
(1, 3, 'FAC-2025-00001', 95.97, 15.36, 111.33, 'Carlos Rodríguez', 'Av. Principal #123, Ciudad', 'RFC-CARLOS-2025');

-- Factura para venta de Luis (sale_id: 2)
INSERT INTO bills (sale_id, user_id, bill_number, subtotal, tax, total, billing_name, billing_address, billing_tax_id) VALUES
(2, 5, 'FAC-2025-00002', 119.48, 19.12, 138.60, 'Luis Fernández', 'Calle Secundaria #456, Ciudad', 'RFC-LUIS-2025');

-- Factura para venta de María (sale_id: 3)
INSERT INTO bills (sale_id, user_id, bill_number, subtotal, tax, total, billing_name, billing_address, billing_tax_id) VALUES
(3, 2, 'FAC-2025-00003', 86.99, 13.92, 100.91, 'María González', 'Blvd. Central #789, Ciudad', 'RFC-MARIA-2025');

-- ====================================
-- VERIFICACIÓN DE DATOS INSERTADOS
-- ====================================

-- Contar registros insertados
DO $$
DECLARE
    users_count INT;
    roles_count INT;
    user_roles_count INT;
    products_count INT;
    carts_count INT;
    cart_items_count INT;
    sales_count INT;
    bills_count INT;
BEGIN
    SELECT COUNT(*) INTO users_count FROM users;
    SELECT COUNT(*) INTO roles_count FROM roles;
    SELECT COUNT(*) INTO user_roles_count FROM user_roles;
    SELECT COUNT(*) INTO products_count FROM products;
    SELECT COUNT(*) INTO carts_count FROM carts;
    SELECT COUNT(*) INTO cart_items_count FROM cart_items;
    SELECT COUNT(*) INTO sales_count FROM sales;
    SELECT COUNT(*) INTO bills_count FROM bills;

    RAISE NOTICE '====================================';
    RAISE NOTICE 'DATOS INSERTADOS EXITOSAMENTE';
    RAISE NOTICE '====================================';
    RAISE NOTICE 'Usuarios: %', users_count;
    RAISE NOTICE 'Roles: %', roles_count;
    RAISE NOTICE 'Asignaciones de roles: %', user_roles_count;
    RAISE NOTICE 'Productos: %', products_count;
    RAISE NOTICE 'Carritos: %', carts_count;
    RAISE NOTICE 'Items en carritos: %', cart_items_count;
    RAISE NOTICE 'Ventas: %', sales_count;
    RAISE NOTICE 'Facturas: %', bills_count;
    RAISE NOTICE '====================================';
END $$;

-- ====================================
-- CONSULTAS DE VERIFICACIÓN
-- ====================================

-- Ver todos los usuarios con sus roles
SELECT
    u.name,
    u.email,
    STRING_AGG(r.name, ', ') AS roles
FROM users u
LEFT JOIN user_roles ur ON u.id = ur.user_id
LEFT JOIN roles r ON ur.role_id = r.id
GROUP BY u.id, u.name, u.email
ORDER BY u.name;

-- Ver resumen de productos por categoría
SELECT
    category,
    COUNT(*) AS total_productos,
    SUM(stock) AS stock_total
FROM products
GROUP BY category
ORDER BY category;

-- Ver carritos activos
SELECT
    u.name AS usuario,
    c.id AS carrito_id,
    COUNT(ci.id) AS items,
    SUM(ci.quantity * ci.price_at_addition) AS total
FROM carts c
INNER JOIN users u ON c.user_id = u.id
LEFT JOIN cart_items ci ON c.id = ci.cart_id
WHERE c.status = 'active'
GROUP BY u.name, c.id;