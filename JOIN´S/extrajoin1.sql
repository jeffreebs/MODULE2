DROP TABLE IF EXISTS All_Numbers;
DROP TABLE IF EXISTS Odd_Numbers;


CREATE TABLE All_Numbers (
    id INTEGER PRIMARY KEY,
    numero INTEGER
);

CREATE TABLE Odd_Numbers (
    id INTEGER PRIMARY KEY,
    numero INTEGER
);


INSERT INTO All_Numbers VALUES
(1, 1),
(2, 2),
(3, 3),
(4, 4),
(5, 5),
(6, 6),
(7, 7),
(8, 8),
(9, 9),
(10, 10);

INSERT INTO Odd_Numbers VALUES
(1, 1),
(3, 3),
(5, 5),
(7, 7),
(9, 9);


SELECT '===== TABLA ALL (TODOS LOS NÚMEROS) =====' AS '';
SELECT * FROM All_Numbers;

SELECT '===== TABLA ODD (NÚMEROS IMPARES) =====' AS '';
SELECT * FROM Odd_Numbers;


SELECT '===== MÉTODO 1: LEFT JOIN + WHERE NULL =====' AS '';
SELECT A.id, A.numero
FROM All_Numbers A
LEFT JOIN Odd_Numbers O ON A.id = O.id
WHERE O.id IS NULL;


SELECT '===== MÉTODO 2: NOT EXISTS =====' AS '';
SELECT A.id, A.numero
FROM All_Numbers A
WHERE NOT EXISTS (
    SELECT 1 
    FROM Odd_Numbers O 
    WHERE O.id = A.id
);


SELECT '===== MÉTODO 3: NOT IN =====' AS '';
SELECT id, numero
FROM All_Numbers
WHERE id NOT IN (SELECT id FROM Odd_Numbers);


SELECT '===== VISUALIZACIÓN DEL LEFT JOIN COMPLETO =====' AS '';
SELECT 
    A.id AS All_ID,
    A.numero AS All_Numero,
    O.id AS Odd_ID,
    O.numero AS Odd_Numero
FROM All_Numbers A
LEFT JOIN Odd_Numbers O ON A.id = O.id;


SELECT '===== OTRAS OPERACIONES DE CONJUNTOS =====' AS '';


SELECT '--- INTERSECCIÓN (A ∩ B): INNER JOIN ---' AS '';
SELECT A.id, A.numero
FROM All_Numbers A
INNER JOIN Odd_Numbers O ON A.id = O.id;


SELECT '--- UNIÓN (A ∪ B): UNION ---' AS '';
SELECT id, numero FROM All_Numbers
UNION
SELECT id, numero FROM Odd_Numbers;


SELECT '--- SOLO EN ODD (B - A): RIGHT JOIN SIMULADO ---' AS '';
SELECT O.id, O.numero
FROM All_Numbers A
RIGHT JOIN Odd_Numbers O ON A.id = O.id
WHERE A.id IS NULL;

SELECT 'Nota: SQLite no soporta RIGHT JOIN, alternativa con LEFT JOIN:' AS '';
SELECT O.id, O.numero
FROM Odd_Numbers O
LEFT JOIN All_Numbers A ON O.id = A.id
WHERE A.id IS NULL;


SELECT '===== COMPARACIÓN DE RESULTADOS =====' AS '';
SELECT 'Operación All - Odd debería dar: {2, 4, 6, 8, 10}' AS '';
SELECT 'Los tres métodos dan el mismo resultado:' AS '';

SELECT 'LEFT JOIN:' AS Metodo, COUNT(*) AS Total FROM (
    SELECT A.id FROM All_Numbers A
    LEFT JOIN Odd_Numbers O ON A.id = O.id
    WHERE O.id IS NULL
);

SELECT 'NOT EXISTS:' AS Metodo, COUNT(*) AS Total FROM (
    SELECT A.id FROM All_Numbers A
    WHERE NOT EXISTS (SELECT 1 FROM Odd_Numbers O WHERE O.id = A.id)
);

SELECT 'NOT IN:' AS Metodo, COUNT(*) AS Total FROM (
    SELECT id FROM All_Numbers WHERE id NOT IN (SELECT id FROM Odd_Numbers)
);