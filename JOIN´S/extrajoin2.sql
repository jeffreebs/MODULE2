DROP TABLE IF EXISTS Books;
DROP TABLE IF EXISTS Customers;
DROP TABLE IF EXISTS Rents;


CREATE TABLE Books (
    book_id INTEGER PRIMARY KEY,
    title TEXT,
    author TEXT,
    year INTEGER
);

CREATE TABLE Customers (
    customer_id INTEGER PRIMARY KEY,
    customer_name TEXT,
    email TEXT
);

CREATE TABLE Rents (
    rent_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    book_id INTEGER,
    rent_date TEXT,
    FOREIGN KEY (customer_id) REFERENCES Customers(customer_id),
    FOREIGN KEY (book_id) REFERENCES Books(book_id)
);


INSERT INTO Books VALUES
(1, 'Cien años de soledad', 'Gabriel García Márquez', 1967),
(2, 'Don Quijote de la Mancha', 'Miguel de Cervantes', 1605),
(3, '1984', 'George Orwell', 1949),
(4, 'El principito', 'Antoine de Saint-Exupéry', 1943),
(5, 'Harry Potter y la piedra filosofal', 'J.K. Rowling', 1997);

INSERT INTO Customers VALUES
(101, 'Ana Rodríguez', 'ana@email.com'),
(102, 'Carlos Méndez', 'carlos@email.com'),
(103, 'Laura Jiménez', 'laura@email.com'),
(104, 'Pedro Sánchez', 'pedro@email.com'),
(105, 'María González', 'maria@email.com');

INSERT INTO Rents VALUES
(1, 101, 1, '2024-01-05'),
(2, 101, 2, '2024-01-15'),
(3, 101, 3, '2024-02-10'),
(4, 101, 4, '2024-03-01'),
(5, 101, 5, '2024-03-15'),
(6, 102, 1, '2024-01-20'),
(7, 102, 3, '2024-02-05'),
(8, 102, 5, '2024-02-25'),
(9, 103, 2, '2024-01-10'),
(10, 103, 4, '2024-02-20'),
(11, 103, 1, '2024-03-10'),
(12, 103, 3, '2024-03-20'),
(13, 104, 5, '2024-01-25'),
(14, 104, 2, '2024-02-15'),
(15, 105, 1, '2024-03-05');


SELECT 'TABLAS BASE' AS '';

SELECT 'Books:' AS '';
SELECT * FROM Books;

SELECT 'Customers:' AS '';
SELECT * FROM Customers;

SELECT 'Rents:' AS '';
SELECT * FROM Rents;


SELECT 'SOLUCIÓN: TOP 3 CLIENTES MÁS ACTIVOS' AS '';

SELECT 
    c.customer_id,
    c.customer_name,
    COUNT(r.rent_id) AS total_rentas
FROM Customers c
INNER JOIN Rents r ON c.customer_id = r.customer_id
GROUP BY c.customer_id, c.customer_name
ORDER BY total_rentas DESC
LIMIT 3;


SELECT 'ANÁLISIS COMPLETO: TODOS LOS CLIENTES' AS '';

SELECT 
    c.customer_id,
    c.customer_name,
    COUNT(r.rent_id) AS total_rentas
FROM Customers c
INNER JOIN Rents r ON c.customer_id = r.customer_id
GROUP BY c.customer_id, c.customer_name
ORDER BY total_rentas DESC;


SELECT 'DESGLOSE POR CLIENTE' AS '';

SELECT 
    c.customer_name,
    b.title AS libro_rentado,
    r.rent_date AS fecha_renta
FROM Customers c
INNER JOIN Rents r ON c.customer_id = r.customer_id
INNER JOIN Books b ON r.book_id = b.book_id
ORDER BY c.customer_name, r.rent_date;


SELECT 'ESTADÍSTICAS ADICIONALES ' AS '';

SELECT 'Total de rentas:' AS Estadistica, COUNT(*) AS Valor FROM Rents
UNION ALL
SELECT 'Total de clientes activos:', COUNT(DISTINCT customer_id) FROM Rents
UNION ALL
SELECT 'Total de libros rentados:', COUNT(DISTINCT book_id) FROM Rents
UNION ALL
SELECT 'Promedio de rentas por cliente:', ROUND(CAST(COUNT(*) AS FLOAT) / COUNT(DISTINCT customer_id), 2) FROM Rents;