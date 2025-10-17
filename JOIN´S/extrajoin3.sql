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


SELECT ' PROBLEMA: ¿Qué pasa si usamos INNER JOIN? ' AS '';
SELECT 'INNER JOIN excluye los libros sin autor (book_id 5)' AS '';

SELECT 
    c.customer_name AS Nombre_Cliente,
    b.title AS Nombre_Libro,
    a.author_name AS Nombre_Autor,
    r.status AS Estado_Alquiler
FROM Rents r
INNER JOIN Customers c ON r.customer_id = c.customer_id
INNER JOIN Books b ON r.book_id = b.book_id
INNER JOIN Authors a ON b.author_id = a.author_id
ORDER BY c.customer_name, r.rent_date;

SELECT 'RESULTADO: Solo 5 rentas (faltan las 2 del libro sin autor)' AS '';


SELECT 'SOLUCIÓN CORRECTA: LEFT JOIN + COALESCE ' AS '';
SELECT 'LEFT JOIN incluye TODOS los libros, incluso sin autor' AS '';

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

SELECT 'RESULTADO: Las 7 rentas completas' AS '';


SELECT ' COMPARACIÓN LADO A LADO ' AS '';

SELECT 'Total de rentas en la base de datos:' AS Descripcion, COUNT(*) AS Cantidad FROM Rents
UNION ALL
SELECT 'Rentas mostradas con INNER JOIN:', 
    (SELECT COUNT(*) FROM Rents r
     INNER JOIN Books b ON r.book_id = b.book_id
     INNER JOIN Authors a ON b.author_id = a.author_id)
UNION ALL
SELECT 'Rentas mostradas con LEFT JOIN:', 
    (SELECT COUNT(*) FROM Rents r
     INNER JOIN Books b ON r.book_id = b.book_id
     LEFT JOIN Authors a ON b.author_id = a.author_id)
UNION ALL
SELECT 'Rentas PERDIDAS con INNER JOIN:', 
    (SELECT COUNT(*) FROM Rents WHERE book_id = 5);


SELECT ' ¿QUIÉNES RENTARON EL LIBRO SIN AUTOR?' AS '';

SELECT 
    c.customer_name AS Cliente,
    b.title AS Libro,
    r.rent_date AS Fecha,
    r.status AS Estado
FROM Rents r
INNER JOIN Customers c ON r.customer_id = c.customer_id
INNER JOIN Books b ON r.book_id = b.book_id
WHERE b.author_id IS NULL
ORDER BY r.rent_date;


SELECT 'ESTADÍSTICA: Libros con y sin autor' AS '';

SELECT 
    CASE 
        WHEN b.author_id IS NULL THEN 'Sin Autor'
        ELSE 'Con Autor'
    END AS Tipo_Libro,
    COUNT(DISTINCT b.book_id) AS Total_Libros,
    COUNT(r.rent_id) AS Total_Rentas
FROM Books b
LEFT JOIN Rents r ON b.book_id = r.book_id
GROUP BY 
    CASE 
        WHEN b.author_id IS NULL THEN 'Sin Autor'
        ELSE 'Con Autor'
    END;


SELECT 'ANÁLISIS: ¿Por qué es importante LEFT JOIN?' AS '';

SELECT 
    'Si Pedro (104) renta "Libro sin autor conocido":' AS Escenario
UNION ALL
SELECT '- Con INNER JOIN: Pedro NO aparece en resultados'
UNION ALL
SELECT '- Con LEFT JOIN: Pedro SÍ aparece con autor = NULL'
UNION ALL
SELECT '- Con LEFT JOIN + COALESCE: Pedro aparece con "Sin autor"'
UNION ALL
SELECT ''
UNION ALL
SELECT 'LEFT JOIN es esencial para NO perder datos';


SELECT 'TU CÓDIGO ESTÁ CORRECTO' AS '';
SELECT ' LEFT JOIN para Authors' AS Verificacion
UNION ALL
SELECT ' COALESCE para manejar NULL'
UNION ALL
SELECT ' Incluye todos los libros, tengan o no autor'
UNION ALL
SELECT ' No pierde información de rentas';