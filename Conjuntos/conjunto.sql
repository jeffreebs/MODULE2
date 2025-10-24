
DROP TABLE IF EXISTS All_Numbers;
DROP TABLE IF EXISTS Even;
DROP TABLE IF EXISTS Odd;


CREATE TABLE All_Numbers (
    number INTEGER PRIMARY KEY
);

INSERT INTO All_Numbers VALUES (1),(2),(3),(4),(5),(6),(7),(8),(9),(10);


CREATE TABLE Even (
    number INTEGER PRIMARY KEY
);

INSERT INTO Even VALUES (2),(4),(6),(8),(10);

CREATE TABLE Odd (
    number INTEGER PRIMARY KEY
);

INSERT INTO Odd VALUES (1),(3),(5),(7),(9);



SELECT '=== TABLE All ===' AS '';
SELECT * FROM All_Numbers;

SELECT '=== TABLE Even ===' AS '';
SELECT * FROM Even;

SELECT '=== TABLE Odd ===' AS '';
SELECT * FROM Odd;



SELECT '=== 1. Even ∪ Odd (UNION) ===' AS '';
SELECT number FROM Even
UNION
SELECT number FROM Odd
ORDER BY number;



SELECT '=== 2. Even ∩ Odd (INTERSECT) ===' AS '';
SELECT number FROM Even
INTERSECT
SELECT number FROM Odd;



SELECT '=== 3. All - Odd (EXCEPT) ===' AS '';
SELECT number FROM All_Numbers
EXCEPT
SELECT number FROM Odd
ORDER BY number;



SELECT '=== 4. C(Even) - Complement of Even ===' AS '';

SELECT number FROM All_Numbers
EXCEPT
SELECT number FROM Even
ORDER BY number;



SELECT '=== 5. C(Odd - All) ===' AS '';

SELECT number FROM All_Numbers
EXCEPT
SELECT number FROM (
    SELECT number FROM Odd
    EXCEPT
    SELECT number FROM All_Numbers
)
ORDER BY number;


SELECT '=== VERIFICATION: Even ∪ Odd = All ===' AS '';
SELECT 
    CASE 
        WHEN COUNT(*) = 10 THEN 'TRUE: Even ∪ Odd contains 10 elements like All'
        ELSE 'FALSE'
    END AS Result
FROM (
    SELECT number FROM Even
    UNION
    SELECT number FROM Odd
);

SELECT '=== VERIFICATION: Even and Odd are disjoint ===' AS '';
SELECT 
    CASE 
        WHEN COUNT(*) = 0 THEN 'TRUE: Even ∩ Odd = ∅ (empty set)'
        ELSE 'FALSE'
    END AS Result
FROM (
    SELECT number FROM Even
    INTERSECT
    SELECT number FROM Odd
);



SELECT '=== SUMMARY OF SQL OPERATIONS ===' AS '';
SELECT 
    'UNION' AS Operation,
    '∪' AS Symbol,
    'Combines results removing duplicates' AS Description
UNION ALL
SELECT 
    'INTERSECT',
    '∩',
    'Returns only common elements'
UNION ALL
SELECT 
    'EXCEPT/MINUS',
    '-',
    'Returns elements from first set that are not in second'
UNION ALL
SELECT 
    'COMPLEMENT',
    'C(A)',
    'All - A (elements that are not in A)';