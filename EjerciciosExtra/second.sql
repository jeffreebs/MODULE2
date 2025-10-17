DROP TABLE IF EXISTS Student_Course_Data_1FN;
DROP TABLE IF EXISTS Students_2FN;
DROP TABLE IF EXISTS Courses_2FN;
DROP TABLE IF EXISTS Enrollments_2FN;
DROP TABLE IF EXISTS Students_3FN;
DROP TABLE IF EXISTS Instructors_3FN;
DROP TABLE IF EXISTS Courses_3FN;
DROP TABLE IF EXISTS Enrollments_3FN;


CREATE TABLE Student_Course_Data_1FN (
    Student_ID INTEGER,
    Student_Name TEXT,
    Course_Code TEXT,
    Course_Name TEXT,
    Instructor_Name TEXT,
    Instructor_Email TEXT,
    PRIMARY KEY (Student_ID, Course_Code)
);

INSERT INTO Student_Course_Data_1FN VALUES
(301, 'Marco Gómez', 'CS101', 'Python I', 'Juan Pérez', 'juan@uni.edu'),
(301, 'Marco Gómez', 'CS102', 'Python II', 'Laura Rojas', 'laura@uni.edu'),
(302, 'Carla Ruiz', 'CS101', 'Python I', 'Juan Pérez', 'juan@uni.edu');


CREATE TABLE Students_2FN (
    Student_ID INTEGER PRIMARY KEY,
    Student_Name TEXT
);

CREATE TABLE Courses_2FN (
    Course_Code TEXT PRIMARY KEY,
    Course_Name TEXT,
    Instructor_Name TEXT,
    Instructor_Email TEXT
);

CREATE TABLE Enrollments_2FN (
    Student_ID INTEGER,
    Course_Code TEXT,
    PRIMARY KEY (Student_ID, Course_Code),
    FOREIGN KEY (Student_ID) REFERENCES Students_2FN(Student_ID),
    FOREIGN KEY (Course_Code) REFERENCES Courses_2FN(Course_Code)
);

INSERT INTO Students_2FN VALUES
(301, 'Marco Gómez'),
(302, 'Carla Ruiz');

INSERT INTO Courses_2FN VALUES
('CS101', 'Python I', 'Juan Pérez', 'juan@uni.edu'),
('CS102', 'Python II', 'Laura Rojas', 'laura@uni.edu');

INSERT INTO Enrollments_2FN VALUES
(301, 'CS101'),
(301, 'CS102'),
(302, 'CS101');


CREATE TABLE Instructors_3FN (
    Instructor_ID INTEGER PRIMARY KEY,
    Instructor_Name TEXT,
    Instructor_Email TEXT
);

CREATE TABLE Students_3FN (
    Student_ID INTEGER PRIMARY KEY,
    Student_Name TEXT
);

CREATE TABLE Courses_3FN (
    Course_Code TEXT PRIMARY KEY,
    Course_Name TEXT,
    Instructor_ID INTEGER,
    FOREIGN KEY (Instructor_ID) REFERENCES Instructors_3FN(Instructor_ID)
);

CREATE TABLE Enrollments_3FN (
    Student_ID INTEGER,
    Course_Code TEXT,
    PRIMARY KEY (Student_ID, Course_Code),
    FOREIGN KEY (Student_ID) REFERENCES Students_3FN(Student_ID),
    FOREIGN KEY (Course_Code) REFERENCES Courses_3FN(Course_Code)
);

INSERT INTO Instructors_3FN VALUES
(1, 'Juan Pérez', 'juan@uni.edu'),
(2, 'Laura Rojas', 'laura@uni.edu');

INSERT INTO Students_3FN VALUES
(301, 'Marco Gómez'),
(302, 'Carla Ruiz');

INSERT INTO Courses_3FN VALUES
('CS101', 'Python I', 1),
('CS102', 'Python II', 2);

INSERT INTO Enrollments_3FN VALUES
(301, 'CS101'),
(301, 'CS102'),
(302, 'CS101');


SELECT 'TABLA ORIGINAL (1FN)' AS '';
SELECT * FROM Student_Course_Data_1FN;

SELECT 'TABLAS EN 2FN' AS '';
SELECT 'Students_2FN:' AS '';
SELECT * FROM Students_2FN;
SELECT 'Courses_2FN:' AS '';
SELECT * FROM Courses_2FN;
SELECT 'Enrollments_2FN:' AS '';
SELECT * FROM Enrollments_2FN;

SELECT 'TABLAS EN 3FN (NORMALIZADAS) ' AS '';
SELECT 'Instructors_3FN:' AS '';
SELECT * FROM Instructors_3FN;
SELECT 'Students_3FN:' AS '';
SELECT * FROM Students_3FN;
SELECT 'Courses_3FN:' AS '';
SELECT * FROM Courses_3FN;
SELECT 'Enrollments_3FN:' AS '';
SELECT * FROM Enrollments_3FN;

SELECT 'CONSULTA EJEMPLO: Estudiantes con sus Cursos e Instructores (3FN)' AS '';
SELECT 
    s.Student_ID,
    s.Student_Name,
    c.Course_Code,
    c.Course_Name,
    i.Instructor_Name,
    i.Instructor_Email
FROM Students_3FN s
INNER JOIN Enrollments_3FN e ON s.Student_ID = e.Student_ID
INNER JOIN Courses_3FN c ON e.Course_Code = c.Course_Code
INNER JOIN Instructors_3FN i ON c.Instructor_ID = i.Instructor_ID
ORDER BY s.Student_ID, c.Course_Code;