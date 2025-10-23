-- SQLite
SELECT *
FROM products;


SELECT *
FROM products 
WHERE price  > 50000;


SELECT *
FROM cart_details
WHERE product_code = "P001" ;


SELECT 
    product_code,
    SUM (quantity) AS total_uni
FROM cart_details
GROUP BY product_code;


SELECT *
FROM bills 
WHERE buyer_email = "prueba@hotmail.com";


SELECT *
FROM bills 
ORDER BY amount DESC;


SELECT *
FROM bills
WHERE invoice_number = "F001";



