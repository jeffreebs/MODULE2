DROP TABLE IF EXISTS ordenes_original;
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS items;
DROP TABLE IF EXISTS orders;


CREATE TABLE ordenes_original (
    order_id TEXT,
    customer_name TEXT,
    customer_phone TEXT,
    address TEXT,  
    item_id TEXT,
    item_name TEXT,
    price REAL,
    quantity INTEGER,
    special_request TEXT,
    delivery_time TEXT
);

INSERT INTO ordenes_original VALUES
('001', 'Alice', '123-456-7890', '123 Main St', '101', 'Cheeseburger', 8, 2, 'No onions', '6:00 PM'),
('001', 'Alice', '123-456-7890', '123 Main St', '102', 'Fries', 3, 1, 'Extra ketchup', '6:00 PM'),
('002', 'Bob', '987-654-3210', '456 Elm St', '103', 'Pizza', 12, 1, 'Extra cheese', '7:30 PM'),
('002', 'Bob', '987-654-3210', '456 Elm St', '104', 'Fries', 2, 2, 'None', '7:30 PM'),
('003', 'Claire', '555-123-4567', '789 Oak St', '105', 'Salad', 6, 1, 'No croutons', '12:00 PM'),
('004', 'Claire', '555-123-4567', '464 Georgia St', '106', 'Water', 1, 1, 'None', '5:00 PM');


CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_name TEXT NOT NULL,
    customer_phone TEXT UNIQUE NOT NULL
);

CREATE TABLE items (
    item_id TEXT PRIMARY KEY,
    item_name TEXT NOT NULL,
    price REAL NOT NULL
);

CREATE TABLE orders (
    order_id TEXT PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    address TEXT NOT NULL,
    delivery_time TEXT,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

CREATE TABLE order_items (
    order_id TEXT,
    item_id TEXT,
    quantity INTEGER NOT NULL,
    special_request TEXT,
    PRIMARY KEY (order_id, item_id),
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (item_id) REFERENCES items(item_id)
);


INSERT INTO customers (customer_name, customer_phone)
SELECT DISTINCT customer_name, customer_phone 
FROM ordenes_original;

INSERT INTO items (item_id, item_name, price)
SELECT DISTINCT item_id, item_name, price 
FROM ordenes_original;

INSERT INTO orders (order_id, customer_id, address, delivery_time)
SELECT DISTINCT 
    o.order_id,
    c.customer_id,
    o.address,
    o.delivery_time
FROM ordenes_original o
JOIN customers c ON o.customer_name = c.customer_name 
                AND o.customer_phone = c.customer_phone;

INSERT INTO order_items (order_id, item_id, quantity, special_request)
SELECT 
    order_id,
    item_id,
    quantity,
    special_request
FROM ordenes_original;


SELECT ' TABLA ORIGINAL ' AS '';
SELECT * FROM ordenes_original;

SELECT 'CUSTOMERS (sin dirección) ' AS '';
SELECT * FROM customers;

SELECT ' ITEMS ' AS '';
SELECT * FROM items;

SELECT 'ORDERS (con dirección y datos generales)' AS '';
SELECT * FROM orders;

SELECT 'ORDER_ITEMS (detalle de items por orden - relación N:N)' AS '';
SELECT * FROM order_items;


SELECT 'CONSULTA COMPLETA: Reconstruir órdenes originales' AS '';
SELECT 
    o.order_id,
    c.customer_name,
    c.customer_phone,
    o.address,
    i.item_id,
    i.item_name,
    i.price,
    oi.quantity,
    oi.special_request,
    o.delivery_time
FROM orders o
INNER JOIN customers c ON o.customer_id = c.customer_id
INNER JOIN order_items oi ON o.order_id = oi.order_id
INNER JOIN items i ON oi.item_id = i.item_id
ORDER BY o.order_id, i.item_id;


SELECT 'ANÁLISIS: Órdenes por cliente' AS '';
SELECT 
    c.customer_name,
    COUNT(DISTINCT o.order_id) AS total_ordenes,
    SUM(i.price * oi.quantity) AS total_gastado
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
INNER JOIN order_items oi ON o.order_id = oi.order_id
INNER JOIN items i ON oi.item_id = i.item_id
GROUP BY c.customer_id, c.customer_name
ORDER BY total_gastado DESC;


SELECT 'ANÁLISIS: Items por orden' AS '';
SELECT 
    o.order_id,
    c.customer_name,
    COUNT(oi.item_id) AS total_items,
    SUM(i.price * oi.quantity) AS total_orden
FROM orders o
INNER JOIN customers c ON o.customer_id = c.customer_id
INNER JOIN order_items oi ON o.order_id = oi.order_id
INNER JOIN items i ON oi.item_id = i.item_id
GROUP BY o.order_id, c.customer_name
ORDER BY o.order_id;