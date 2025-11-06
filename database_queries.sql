
SELECT
    c.id AS cart_id,
    c.user_id,
    u.name AS user_name,
    u.email AS user_email,
    c.status,
    c.created_at,
    c.updated_at
FROM carts c
INNER JOIN users u ON c.user_id = u.id
WHERE c.user_id = 1  
  AND c.status = 'active';


SELECT
    c.id AS cart_id,
    c.user_id,
    u.name AS user_name,
    u.email AS user_email,
    c.status,
    ci.id AS item_id,
    p.name AS product_name,
    p.sku,
    ci.quantity,
    ci.price_at_addition,
    (ci.quantity * ci.price_at_addition) AS subtotal_item,
    c.created_at,
    c.updated_at
FROM carts c
INNER JOIN users u ON c.user_id = u.id
LEFT JOIN cart_items ci ON c.id = ci.cart_id
LEFT JOIN products p ON ci.product_id = p.id
WHERE c.user_id = 1  -- Cambiar por el ID del usuario deseado
  AND c.status = 'active'
ORDER BY ci.added_at DESC;



SELECT
    b.id AS bill_id,
    b.bill_number,
    b.user_id,
    u.name AS user_name,
    u.email AS user_email,
    b.subtotal,
    b.tax,
    b.total,
    b.billing_name,
    b.billing_address,
    b.billing_tax_id,
    b.created_at AS bill_date,
    s.sale_date,
    s.payment_method
FROM bills b
INNER JOIN users u ON b.user_id = u.id
INNER JOIN sales s ON b.sale_id = s.id
WHERE b.user_id = 1  
ORDER BY b.created_at DESC;



SELECT
    b.id AS bill_id,
    b.bill_number,
    b.total AS bill_total,
    p.id AS product_id,
    p.sku,
    p.name AS product_name,
    ci.quantity,
    ci.price_at_addition AS unit_price,
    (ci.quantity * ci.price_at_addition) AS subtotal_product
FROM bills b
INNER JOIN sales s ON b.sale_id = s.id
INNER JOIN carts c ON s.cart_id = c.id
INNER JOIN cart_items ci ON c.id = ci.cart_id
INNER JOIN products p ON ci.product_id = p.id
WHERE b.id = 1  
ORDER BY p.name;


SELECT
    u.id AS user_id,
    u.name AS user_name,
    u.email,
    r.id AS role_id,
    r.name AS role_name,
    r.description AS role_description,
    ur.assigned_at
FROM users u
INNER JOIN user_roles ur ON u.id = ur.user_id
INNER JOIN roles r ON ur.role_id = r.id
WHERE u.id = 1 
ORDER BY r.name;



SELECT
    u.id AS user_id,
    u.name AS user_name,
    u.email,
    r.name AS role_name,
    ur.assigned_at
FROM users u
INNER JOIN user_roles ur ON u.id = ur.user_id
INNER JOIN roles r ON ur.role_id = r.id
WHERE r.name = 'cliente'  -- Cambiar por el rol deseado (admin, cliente, vendedor)
ORDER BY u.name;



SELECT
    c.id AS cart_id,
    c.user_id,
    u.name AS user_name,
    c.status,
    COUNT(ci.id) AS total_items,
    COALESCE(SUM(ci.quantity * ci.price_at_addition), 0) AS cart_total,
    c.created_at,
    c.completed_at
FROM carts c
INNER JOIN users u ON c.user_id = u.id
LEFT JOIN cart_items ci ON c.id = ci.cart_id
WHERE c.user_id = 1  -- Cambiar por el ID del usuario deseado
GROUP BY c.id, c.user_id, u.name, c.status, c.created_at, c.completed_at
ORDER BY c.created_at DESC;



SELECT
    s.id AS sale_id,
    s.sale_date,
    s.payment_method,
    u.name AS customer_name,
    u.email AS customer_email,
    s.subtotal,
    s.tax,
    s.total,
    p.sku,
    p.name AS product_name,
    ci.quantity,
    ci.price_at_addition AS unit_price,
    (ci.quantity * ci.price_at_addition) AS subtotal_product
FROM sales s
INNER JOIN users u ON s.user_id = u.id
INNER JOIN carts c ON s.cart_id = c.id
INNER JOIN cart_items ci ON c.id = ci.cart_id
INNER JOIN products p ON ci.product_id = p.id
WHERE s.id = 1  -- Cambiar por el ID de la venta deseada
ORDER BY p.name;



SELECT
    p.id AS product_id,
    p.sku,
    p.name AS product_name,
    p.category,
    COUNT(ci.id) AS times_sold,
    SUM(ci.quantity) AS total_quantity_sold,
    SUM(ci.quantity * ci.price_at_addition) AS total_revenue
FROM products p
INNER JOIN cart_items ci ON p.id = ci.product_id
INNER JOIN carts c ON ci.cart_id = c.id
INNER JOIN sales s ON c.id = s.cart_id
GROUP BY p.id, p.sku, p.name, p.category
ORDER BY total_quantity_sold DESC
LIMIT 10;



SELECT
    u.id AS user_id,
    u.name AS customer_name,
    u.email,
    COUNT(s.id) AS total_purchases,
    SUM(s.total) AS total_spent,
    MAX(s.sale_date) AS last_purchase_date,
    MIN(s.sale_date) AS first_purchase_date
FROM users u
INNER JOIN sales s ON u.id = s.user_id
GROUP BY u.id, u.name, u.email
ORDER BY total_spent DESC;



SELECT
    p.id,
    p.sku,
    p.name,
    p.category,
    p.stock,
    p.price,
    p.is_active
FROM products p
WHERE p.stock < 10
  AND p.is_active = TRUE
ORDER BY p.stock ASC;



SELECT
    DATE(s.sale_date) AS sale_day,
    COUNT(s.id) AS total_sales,
    SUM(s.subtotal) AS total_subtotal,
    SUM(s.tax) AS total_tax,
    SUM(s.total) AS total_revenue
FROM sales s
GROUP BY DATE(s.sale_date)
ORDER BY sale_day DESC;



SELECT
    c.id AS cart_id,
    u.name AS user_name,
    u.email,
    COUNT(ci.id) AS items_count,
    SUM(ci.quantity * ci.price_at_addition) AS potential_revenue,
    c.created_at,
    c.updated_at,
    EXTRACT(DAY FROM (CURRENT_TIMESTAMP - c.updated_at)) AS days_abandoned
FROM carts c
INNER JOIN users u ON c.user_id = u.id
LEFT JOIN cart_items ci ON c.id = ci.cart_id
WHERE c.status = 'abandoned'
GROUP BY c.id, u.name, u.email, c.created_at, c.updated_at
ORDER BY c.updated_at DESC;



SELECT
    b.bill_number AS "Número de Factura",
    b.created_at AS "Fecha de Emisión",
    b.billing_name AS "Cliente",
    b.billing_address AS "Dirección",
    b.billing_tax_id AS "RFC/ID Fiscal",
    p.name AS "Producto",
    p.sku AS "SKU",
    ci.quantity AS "Cantidad",
    ci.price_at_addition AS "Precio Unitario",
    (ci.quantity * ci.price_at_addition) AS "Subtotal",
    b.subtotal AS "Subtotal Total",
    b.tax AS "Impuestos",
    b.total AS "Total a Pagar",
    s.payment_method AS "Método de Pago"
FROM bills b
INNER JOIN sales s ON b.sale_id = s.id
INNER JOIN carts c ON s.cart_id = c.id
INNER JOIN cart_items ci ON c.id = ci.cart_id
INNER JOIN products p ON ci.product_id = p.id
WHERE b.id = 1  -- Cambiar por el ID de la factura deseada
ORDER BY p.name;


-
SELECT
    p.category,
    COUNT(p.id) AS total_products,
    SUM(p.stock) AS total_stock,
    AVG(p.price) AS average_price,
    MIN(p.price) AS min_price,
    MAX(p.price) AS max_price
FROM products p
WHERE p.is_active = TRUE
GROUP BY p.category
ORDER BY total_products DESC;



SELECT
    s.id AS sale_id,
    s.subtotal,
    s.tax,
    s.total,
    (s.subtotal + s.tax) AS calculated_total,
    CASE
        WHEN s.total = (s.subtotal + s.tax) THEN 'OK'
        ELSE 'ERROR'
    END AS validation
FROM sales s;


SELECT
    user_id,
    COUNT(*) AS active_carts,
    CASE
        WHEN COUNT(*) = 1 THEN 'OK'
        WHEN COUNT(*) = 0 THEN 'No tiene carrito activo'
        ELSE 'ERROR: Más de un carrito activo'
    END AS validation
FROM carts
WHERE status = 'active'
GROUP BY user_id;



DO $$
BEGIN
    RAISE NOTICE 'Archivo de queries cargado exitosamente!';
    RAISE NOTICE 'Total de queries disponibles: 15';
END $$;
