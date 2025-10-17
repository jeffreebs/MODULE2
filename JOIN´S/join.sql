

DROP TABLE IF EXISTS Rents;
DROP TABLE IF EXISTS Customers;
DROP TABLE IF EXISTS Books;
DROP TABLE IF EXISTS Authors;


CREATE TABLE Authors (
    ID INTEGER PRIMARY KEY,
    Name TEXT NOT NULL
);


CREATE TABLE Books (
    ID INTEGER PRIMARY KEY,
    Name TEXT NOT NULL,
    Author INTEGER,
    FOREIGN KEY (Author) REFERENCES Authors(ID)
);


CREATE TABLE Customers (
    ID INTEGER PRIMARY KEY,
    Name TEXT NOT NULL,
    Email TEXT
);


CREATE TABLE Rents (
    ID INTEGER PRIMARY KEY,
    BookID INTEGER,
    CustomerID INTEGER,
    State TEXT,
    FOREIGN KEY (BookID) REFERENCES Books(ID),
    FOREIGN KEY (CustomerID) REFERENCES Customers(ID)
);


INSERT INTO Authors (ID, Name) VALUES
(1, 'Miguel de Cervantes'),
(2, 'Dante Alighieri'),
(3, 'Takehiko Inoue'),
(4, 'Akira Toriyama'),
(5, 'Walt Disney');


INSERT INTO Books (ID, Name, Author) VALUES
(1, 'Don Quijote', 1),
(2, 'La Divina Comedia', 2),
(3, 'Vagabond 1-3', 3),
(4, 'Dragon Ball 1', 4),
(5, 'The Book of the 5 Rings', NULL);

INSERT INTO Customers (ID, Name, Email) VALUES
(1, 'John Doe', 'j.doe@email.com'),
(2, 'Jane Doe', 'jane@doe.com'),
(3, 'Luke Skywalker', 'darth.son@email.com');


INSERT INTO Rents (ID, BookID, CustomerID, State) VALUES
(1, 1, 2, 'Returned'),
(2, 2, 2, 'Returned'),
(3, 1, 1, 'On time'),
(4, 3, 1, 'On time'),
(5, 2, 2, 'Overdue');


SELECT 'CONSULTA 1: TODOS LOS LIBROS Y SUS AUTORES' AS titulo;

SELECT 
    b.ID AS BookID,
    b.Name AS BookName,
    a.ID AS AuthorID,
    a.Name AS AuthorName
FROM Books b
LEFT JOIN Authors a ON b.Author = a.ID;



SELECT 'CONSULTA 2: LIBROS QUE NO TIENEN AUTOR' AS titulo;

SELECT 
    ID,
    Name
FROM Books
WHERE Author IS NULL;



SELECT 'CONSULTA 3: AUTORES QUE NO TIENEN LIBROS' AS titulo;

SELECT 
    a.ID,
    a.Name
FROM Authors a
LEFT JOIN Books b ON a.ID = b.Author
WHERE b.ID IS NULL;



SELECT 'CONSULTA 4: LIBROS QUE HAN SIDO RENTADOS' AS titulo;

SELECT DISTINCT
    b.ID,
    b.Name
FROM Books b
INNER JOIN Rents r ON b.ID = r.BookID
ORDER BY b.ID;


SELECT 'CONSULTA 5: LIBROS QUE NUNCA HAN SIDO RENTADOS' AS titulo;

SELECT 
    b.ID,
    b.Name
FROM Books b
LEFT JOIN Rents r ON b.ID = r.BookID
WHERE r.ID IS NULL;



SELECT 'CONSULTA 6: CLIENTES QUE NUNCA HAN RENTADO' AS titulo;

SELECT 
    c.ID,
    c.Name,
    c.Email
FROM Customers c
LEFT JOIN Rents r ON c.ID = r.CustomerID
WHERE r.ID IS NULL;



SELECT 'CONSULTA 7: LIBROS EN ESTADO OVERDUE' AS titulo;

SELECT DISTINCT
    b.ID,
    b.Name,
    r.State
FROM Books b
INNER JOIN Rents r ON b.ID = r.BookID
WHERE r.State = 'Overdue';



SELECT 'VERIFICACION: TABLA Authors' AS titulo;
SELECT * FROM Authors;

SELECT 'VERIFICACION: TABLA Books' AS titulo;
SELECT * FROM Books;

SELECT 'VERIFICACION: TABLA Customers' AS titulo;
SELECT * FROM Customers;

SELECT 'VERIFICACION: TABLA Rents' AS titulo;
SELECT * FROM Rents;