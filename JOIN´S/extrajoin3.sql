DROP TABLE IF EXISTS Authors;
DROP TABLE IF EXISTS Books;
DROP TABLE IF EXISTS Customers;
DROP TABLE IF EXISTS Rents;


CREATE TABLE Authors (
    author_id INTEGER PRIMARY KEY,
    author_name TEXT,
    nationality TEXT
);

CREATE TABLE Books (
    book_id INTEGER PRIMARY KEY,
    title TEXT,
    author_id INTEGER,
    year INTEGER,
    FOREIGN KEY (author_id) REFERENCES Authors(author_id)
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
    status TEXT,
    FOREIGN KEY (customer_id) REFERENCES Customers(customer_id),
    FOREIGN KEY (book_id) REFERENCES Books(book_id)
);


INSERT INTO Authors VALUES
(1, 'Gabriel García Márquez', 'Colombiano'),
(2, 'Miguel de Cervantes', 'Español'),
(3, 'George Orwell', 'Británico'),
(4, 'Antoine de Saint-Exupéry', 'Francés');

INSERT INTO Books VALUES
(1, 'Cien años de soledad', 1, 1967),
(2, 'Don Quijote de la Mancha', 2, 1605),
(3, '1984', 3, 1949),
(4, 'El principito', 4, 1943),
(5, 'Libro sin autor conocido', NULL, 2000);

INSERT INTO Customers VALUES
(101, 'Ana Rodríguez', 'ana@email.com'),
(102, 'Carlos Méndez', 'carlos@email.com'),
(103, 'Laura Jiménez', 'laura@email.com'),
(104, 'Pedro Sánchez', 'pedro@email.com');

INSERT INTO Rents VALUES
(1, 101, 1, '2024-01-05', 'Activo'),
(2, 101, 2, '2024-01-15', 'Devuelto'),
(3, 102, 3, '2024-02-10', 'Activo'),
(4, 103, 4, '2024-03-01', 'Retrasado'),
(5, 104, 5, '2024-03-15', 'Activo'),
(6, 102, 1, '2024-02-20', 'Devuelto'),
(7, 103, 5, '2024-03-10', 'Activo');


SELECT ' TABLAS BASE' AS '';

SELECT 'Authors:' AS '';
SELECT * FROM Authors;

SELECT 'Books:' AS '';
SELECT * FROM Books;

SELECT 'Customers:' AS '';
SELECT * FROM Customers;

SELECT 'Rents:' AS '';
SELECT * FROM Rents;


SELECT ' SOLUCIÓN: CONSULTA CON MÚLTIPLES JOINS ' AS '';

SELECT 
    c.customer_name AS Nombre_Cliente,
    b.title AS Nombre_Libro,
    COALESCE(a.author_name, 'Sin autor') AS Nombre_Autor,
    r.status AS Estado_Alquiler
FROM Rents r
INNER JOIN Customers c ON r.customer_id = c.customer_id
INNER JOIN Books b ON r.book_id = b.book_id
LEFT JOIN Authors a ON b.author_id = a.author_id
ORDER BY c.customer_name, r.rent_date;


SELECT ' SOLO ALQUILERES ACTIVOS ' AS '';

SELECT 
    c.customer_name AS Nombre_Cliente,
    b.title AS Nombre_Libro,
    COALESCE(a.author_name, 'Sin autor') AS Nombre_Autor,
    r.status AS Estado_Alquiler
FROM Rents r
INNER JOIN Customers c ON r.customer_id = c.customer_id
INNER JOIN Books b ON r.book_id = b.book_id
LEFT JOIN Authors a ON b.author_id = a.author_id
WHERE r.status = 'Activo'
ORDER BY c.customer_name;


SELECT 'LIBROS SIN AUTOR ' AS '';

SELECT 
    c.customer_name AS Nombre_Cliente,
    b.title AS Nombre_Libro,
    COALESCE(a.author_name, 'Sin autor') AS Nombre_Autor,
    r.status AS Estado_Alquiler
FROM Rents r
INNER JOIN Customers c ON r.customer_id = c.customer_id
INNER JOIN Books b ON r.book_id = b.book_id
LEFT JOIN Authors a ON b.author_id = a.author_id
WHERE b.author_id IS NULL
ORDER BY c.customer_name;


SELECT 'ESTADÍSTICAS POR ESTADO ' AS '';

SELECT 
    r.status AS Estado,
    COUNT(*) AS Total_Alquileres,
    COUNT(DISTINCT c.customer_id) AS Clientes_Diferentes
FROM Rents r
INNER JOIN Customers c ON r.customer_id = c.customer_id
GROUP BY r.status
ORDER BY Total_Alquileres DESC;


SELECT 'CLIENTES CON LIBROS SIN AUTOR' AS '';

SELECT DISTINCT
    c.customer_name AS Cliente,
    COUNT(r.rent_id) AS Libros_Sin_Autor_Rentados
FROM Rents r
INNER JOIN Customers c ON r.customer_id = c.customer_id
INNER JOIN Books b ON r.book_id = b.book_id
WHERE b.author_id IS NULL
GROUP BY c.customer_id, c.customer_name
ORDER BY Libros_Sin_Autor_Rentados DESC;