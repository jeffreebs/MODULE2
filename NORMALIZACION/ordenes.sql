DROP TABLE IF EXISTS ordenes_original;

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


DROP TABLE IF EXISTS customers;
CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_name TEXT NOT NULL,
    customer_phone TEXT,
    address TEXT
);

DROP TABLE IF EXISTS items;  
CREATE TABLE items (
    item_id TEXT PRIMARY KEY,
    item_name TEXT NOT NULL,
    price REAL NOT NULL
);

DROP TABLE IF EXISTS orders;
CREATE TABLE orders (
    order_id TEXT,
    customer_id INTEGER,
    item_id TEXT,
    quantity INTEGER,
    special_request TEXT,
    delivery_time TEXT,
    PRIMARY KEY (order_id, item_id),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (item_id) REFERENCES items(item_id)
);


INSERT INTO customers (customer_name, customer_phone, address)
SELECT DISTINCT customer_name, customer_phone, address 
FROM ordenes_original;

INSERT INTO items (item_id, item_name, price)
SELECT DISTINCT item_id, item_name, price 
FROM ordenes_original;

INSERT INTO orders (order_id, customer_id, item_id, quantity, special_request, delivery_time)
SELECT 
    o.order_id,
    c.customer_id,  
    o.item_id,
    o.quantity,
    o.special_request,
    o.delivery_time
FROM ordenes_original o
JOIN customers c ON o.customer_name = c.customer_name 
                AND o.customer_phone = c.customer_phone 
                AND o.address = c.address;


SELECT * FROM customers;
SELECT * FROM items;  
SELECT * FROM orders;