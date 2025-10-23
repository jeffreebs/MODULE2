


CREATE TABLE products (
    code VARCHAR PRIMARY KEY,
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR NOT NULL,
    price DECIMAL NOT NULL CHECK (price >= 0),
    brand VARCHAR
);


CREATE TABLE cart_details(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cart_id INTEGER NOT NULL,
    product_code VARCHAR NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    FOREIGN KEY (cart_id) REFERENCES cart(id) ON DELETE CASCADE,
    FOREIGN KEY (product_code) REFERENCES products(code) ON UPDATE CASCADE
);


CREATE TABLE invoice_details (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    invoice_number INTEGER NOT NULL,
    product_code VARCHAR NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    subtotal DECIMAL NOT NULL CHECK (subtotal >= 0),
    FOREIGN KEY (invoice_number) REFERENCES bills (invoice_number) ON DELETE CASCADE,
    FOREIGN KEY (product_code) REFERENCES products(code) ON UPDATE CASCADE
);


CREATE TABLE employees (
    code INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL
);


CREATE TABLE cart (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    buyer_email TEXT NOT NULL,
    created_at TEXT DEFAULT (datetime('now'))
);


CREATE TABLE bills (
    invoice_number TEXT PRIMARY KEY,
    purchase_date DATETIME,
    buyer_email TEXT,
    amount DECIMAL CHECK (amount >= 0),
    phone TEXT,
    employee_code INTEGER,
    FOREIGN KEY (employee_code) REFERENCES employees(code) ON DELETE SET NULL
);

INSERT INTO products (code, name, price, brand) VALUES('P001', 'Producto A', 25000, 'Marca1');
INSERT INTO products (code, name, price, brand) VALUES('P002', 'Producto B', 75000, 'Marca2');
INSERT INTO products (code, name, price, brand) VALUES('P003', 'Producto C', 45000, 'Marca3');


INSERT INTO cart (buyer_email) VALUES('prueba@hotmail.com');
INSERT INTO cart (buyer_email) VALUES('usuario@gmail.com');

INSERT INTO cart_details (cart_id, product_code, quantity) VALUES(1, 'P001', 2);
INSERT INTO cart_details (cart_id, product_code, quantity) VALUES(1, 'P002', 1);
INSERT INTO cart_details (cart_id, product_code, quantity) VALUES(2, 'P001', 3);


INSERT INTO bills VALUES('F001', '2023-08-01 10:30:00', 'prueba@hotmail.com', 125000, '555-1234', NULL);
INSERT INTO bills VALUES('F002', '2023-08-02 14:45:00', 'usuario@gmail.com', 75000, '555-5678', NULL);




CREATE TABLE categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    description TEXT
);


CREATE TABLE products_extra (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code VARCHAR NOT NULL UNIQUE,
    product_name TEXT NOT NULL,
    price INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    category_id INTEGER REFERENCES categories(id)
);


CREATE TABLE invoices (
    invoice_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer TEXT NOT NULL,
    total INTEGER NOT NULL CHECK(total >= 0),
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    phone TEXT,
    cashier_code TEXT NOT NULL DEFAULT 'N/A'
);

INSERT INTO categories (name, description) VALUES('Electronics','Phone, laptops, gadgets');
INSERT INTO categories (name, description) VALUES('Groceries','Food, beverage, daily goods');
INSERT INTO categories (name, description) VALUES('Accessories','Cases, chargers, add-ons');

INSERT INTO products_extra (code, product_name, price, quantity, category_id) VALUES('PE001','Apple iPhone Case',12000,15,3);
INSERT INTO products_extra (code, product_name, price, quantity, category_id) VALUES('PE002','USB-C Charger 30W',9100,8,3);
INSERT INTO products_extra (code, product_name, price, quantity, category_id) VALUES('PE003','Gaming Laptop',650100,2,1);
INSERT INTO products_extra (code, product_name, price, quantity, category_id) VALUES('PE004','4K Monitor 27"',220100,5,1);
INSERT INTO products_extra (code, product_name, price, quantity, category_id) VALUES('PE005','Green apple (1kg)',1800,40,2);
INSERT INTO products_extra (code, product_name, price, quantity, category_id) VALUES('PE006','Pineapple Juice 1L',1600,25,2);
INSERT INTO products_extra (code, product_name, price, quantity, category_id) VALUES('PE007','Bluetooth Headphones',45000,12,1);
INSERT INTO products_extra (code, product_name, price, quantity, category_id) VALUES('PE008','Smart TV 55"',380100,2,1);
INSERT INTO products_extra (code, product_name, price, quantity, category_id) VALUES('PE009','Mechanical Keyboard',52100,9,1);
INSERT INTO products_extra (code, product_name, price, quantity, category_id) VALUES('PE010','Phone Tripod',7000,30,3);

INSERT INTO invoices (customer, total, created_at, phone, cashier_code) VALUES('Alice',120000,'2025-08-20 21:44:39','2479-1111','A01');
INSERT INTO invoices (customer, total, created_at, phone, cashier_code) VALUES('Bob',45000,'2025-08-20 21:44:39','2479-1111','A01');
INSERT INTO invoices (customer, total, created_at, phone, cashier_code) VALUES('Carol',78000,'2025-08-20 21:44:39','2479-1111','A01');
INSERT INTO invoices (customer, total, created_at, phone, cashier_code) VALUES('Dave',30000,'2025-08-20 21:44:39','8888-0000','B07');
INSERT INTO invoices (customer, total, created_at, phone, cashier_code) VALUES('Eve',155000,'2025-08-20 21:44:39','8888-0000','B07');





SELECT * FROM products;


SELECT * FROM products WHERE price > 50000;


SELECT * FROM invoice_details WHERE product_code = "P001";


SELECT
    product_code,
    SUM(quantity) AS total_uni
FROM invoice_details
GROUP BY product_code;


SELECT * FROM bills WHERE buyer_email = "prueba@hotmail.com";


SELECT * FROM bills ORDER BY amount DESC;


SELECT * FROM bills WHERE invoice_number = "F001";


PRAGMA table_info(invoices);


SELECT * FROM invoices WHERE phone IS NULL OR phone = '';


SELECT * FROM invoices WHERE invoice_id = 5;


UPDATE products_extra
SET price = 13500
WHERE code = 'PE001';


UPDATE products_extra
SET quantity = quantity + 10
WHERE category_id = 1;


UPDATE invoices
SET phone = '2479-2222'
WHERE customer = 'Alice';


UPDATE products_extra
SET category_id = 2
WHERE code = 'PE005';


UPDATE products_extra
SET price = price * 1.15
WHERE category_id = 3;