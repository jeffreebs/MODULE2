DROP TABLE IF EXISTS Employee_Project_Data_1FN;
DROP TABLE IF EXISTS Employees_2FN;
DROP TABLE IF EXISTS Projects_2FN;
DROP TABLE IF EXISTS Employee_Projects_2FN;
DROP TABLE IF EXISTS Employees_3FN;
DROP TABLE IF EXISTS Departments_3FN;
DROP TABLE IF EXISTS Projects_3FN;
DROP TABLE IF EXISTS Employee_Projects_3FN;


CREATE TABLE Employee_Project_Data_1FN (
    Employee_ID INTEGER,
    Employee_Name TEXT,
    Department TEXT,
    Department_Phone TEXT,
    Project_ID TEXT,
    Project_Name TEXT,
    Project_Budget INTEGER,
    PRIMARY KEY (Employee_ID, Project_ID)
);

INSERT INTO Employee_Project_Data_1FN VALUES
(201, 'Ana Rivera', 'IT', '2222-2222', 'P001', 'Web App', 50000),
(201, 'Ana Rivera', 'IT', '2222-2222', 'P002', 'API REST', 25000),
(202, 'Luis Mendez', 'Marketing', '1111-1111', 'P003', 'Campaña TV', 30000);


CREATE TABLE Employees_2FN (
    Employee_ID INTEGER PRIMARY KEY,
    Employee_Name TEXT,
    Department TEXT,
    Department_Phone TEXT
);

CREATE TABLE Projects_2FN (
    Project_ID TEXT PRIMARY KEY,
    Project_Name TEXT,
    Project_Budget INTEGER
);

CREATE TABLE Employee_Projects_2FN (
    Employee_ID INTEGER,
    Project_ID TEXT,
    PRIMARY KEY (Employee_ID, Project_ID),
    FOREIGN KEY (Employee_ID) REFERENCES Employees_2FN(Employee_ID),
    FOREIGN KEY (Project_ID) REFERENCES Projects_2FN(Project_ID)
);

INSERT INTO Employees_2FN VALUES
(201, 'Ana Rivera', 'IT', '2222-2222'),
(202, 'Luis Mendez', 'Marketing', '1111-1111');

INSERT INTO Projects_2FN VALUES
('P001', 'Web App', 50000),
('P002', 'API REST', 25000),
('P003', 'Campaña TV', 30000);

INSERT INTO Employee_Projects_2FN VALUES
(201, 'P001'),
(201, 'P002'),
(202, 'P003');


CREATE TABLE Departments_3FN (
    Department_ID INTEGER PRIMARY KEY,
    Department_Name TEXT,
    Department_Phone TEXT
);

CREATE TABLE Employees_3FN (
    Employee_ID INTEGER PRIMARY KEY,
    Employee_Name TEXT,
    Department_ID INTEGER,
    FOREIGN KEY (Department_ID) REFERENCES Departments_3FN(Department_ID)
);

CREATE TABLE Projects_3FN (
    Project_ID TEXT PRIMARY KEY,
    Project_Name TEXT,
    Project_Budget INTEGER
);

CREATE TABLE Employee_Projects_3FN (
    Employee_ID INTEGER,
    Project_ID TEXT,
    PRIMARY KEY (Employee_ID, Project_ID),
    FOREIGN KEY (Employee_ID) REFERENCES Employees_3FN(Employee_ID),
    FOREIGN KEY (Project_ID) REFERENCES Projects_3FN(Project_ID)
);

INSERT INTO Departments_3FN VALUES
(1, 'IT', '2222-2222'),
(2, 'Marketing', '1111-1111');

INSERT INTO Employees_3FN VALUES
(201, 'Ana Rivera', 1),
(202, 'Luis Mendez', 2);

INSERT INTO Projects_3FN VALUES
('P001', 'Web App', 50000),
('P002', 'API REST', 25000),
('P003', 'Campaña TV', 30000);

INSERT INTO Employee_Projects_3FN VALUES
(201, 'P001'),
(201, 'P002'),
(202, 'P003');


SELECT 'TABLA ORIGINAL (1FN) ' AS '';
SELECT * FROM Employee_Project_Data_1FN;

SELECT 'TABLAS EN 2FN ' AS '';
SELECT 'Employees_2FN:' AS '';
SELECT * FROM Employees_2FN;
SELECT 'Projects_2FN:' AS '';
SELECT * FROM Projects_2FN;
SELECT 'Employee_Projects_2FN:' AS '';
SELECT * FROM Employee_Projects_2FN;

SELECT ' TABLAS EN 3FN (NORMALIZADAS) ' AS '';
SELECT 'Departments_3FN:' AS '';
SELECT * FROM Departments_3FN;
SELECT 'Employees_3FN:' AS '';
SELECT * FROM Employees_3FN;
SELECT 'Projects_3FN:' AS '';
SELECT * FROM Projects_3FN;
SELECT 'Employee_Projects_3FN:' AS '';
SELECT * FROM Employee_Projects_3FN;

SELECT 'CONSULTA EJEMPLO: Empleados con sus Departamentos y Proyectos (3FN) ' AS '';
SELECT 
    e.Employee_ID,
    e.Employee_Name,
    d.Department_Name,
    d.Department_Phone,
    p.Project_ID,
    p.Project_Name,
    p.Project_Budget
FROM Employees_3FN e
INNER JOIN Departments_3FN d ON e.Department_ID = d.Department_ID
INNER JOIN Employee_Projects_3FN ep ON e.Employee_ID = ep.Employee_ID
INNER JOIN Projects_3FN p ON ep.Project_ID = p.Project_ID
ORDER BY e.Employee_ID, p.Project_ID;