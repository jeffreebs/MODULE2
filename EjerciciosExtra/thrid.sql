DROP TABLE IF EXISTS Appointments_1FN;
DROP TABLE IF EXISTS Appointments_2FN;
DROP TABLE IF EXISTS Patients_3FN;
DROP TABLE IF EXISTS Doctors_3FN;
DROP TABLE IF EXISTS Appointments_3FN;


CREATE TABLE Appointments_1FN (
    Appointment_ID TEXT PRIMARY KEY,
    Patient_Name TEXT,
    Patient_Phone TEXT,
    Doctor_Name TEXT,
    Specialty TEXT,
    Date TEXT,
    Time TEXT
);

INSERT INTO Appointments_1FN VALUES
('A01', 'Diana Vargas', '8888-1111', 'Dr. Soto', 'Pediatría', '2024-08-01', '10:00 AM'),
('A02', 'Diana Vargas', '8888-1111', 'Dr. Soto', 'Pediatría', '2024-08-10', '10:00 AM'),
('A03', 'Edwin Mora', '8999-2222', 'Dr. Mora', 'Cardiología', '2024-08-05', '01:00 PM');


CREATE TABLE Appointments_2FN (
    Appointment_ID TEXT PRIMARY KEY,
    Patient_Name TEXT,
    Patient_Phone TEXT,
    Doctor_Name TEXT,
    Specialty TEXT,
    Date TEXT,
    Time TEXT
);

INSERT INTO Appointments_2FN VALUES
('A01', 'Diana Vargas', '8888-1111', 'Dr. Soto', 'Pediatría', '2024-08-01', '10:00 AM'),
('A02', 'Diana Vargas', '8888-1111', 'Dr. Soto', 'Pediatría', '2024-08-10', '10:00 AM'),
('A03', 'Edwin Mora', '8999-2222', 'Dr. Mora', 'Cardiología', '2024-08-05', '01:00 PM');


CREATE TABLE Patients_3FN (
    Patient_ID INTEGER PRIMARY KEY,
    Patient_Name TEXT,
    Patient_Phone TEXT
);

CREATE TABLE Doctors_3FN (
    Doctor_ID INTEGER PRIMARY KEY,
    Doctor_Name TEXT,
    Specialty TEXT
);

CREATE TABLE Appointments_3FN (
    Appointment_ID TEXT PRIMARY KEY,
    Patient_ID INTEGER,
    Doctor_ID INTEGER,
    Date TEXT,
    Time TEXT,
    FOREIGN KEY (Patient_ID) REFERENCES Patients_3FN(Patient_ID),
    FOREIGN KEY (Doctor_ID) REFERENCES Doctors_3FN(Doctor_ID)
);

INSERT INTO Patients_3FN VALUES
(1, 'Diana Vargas', '8888-1111'),
(2, 'Edwin Mora', '8999-2222');

INSERT INTO Doctors_3FN VALUES
(1, 'Dr. Soto', 'Pediatría'),
(2, 'Dr. Mora', 'Cardiología');

INSERT INTO Appointments_3FN VALUES
('A01', 1, 1, '2024-08-01', '10:00 AM'),
('A02', 1, 1, '2024-08-10', '10:00 AM'),
('A03', 2, 2, '2024-08-05', '01:00 PM');


SELECT 'TABLA ORIGINAL (1FN) ' AS '';
SELECT * FROM Appointments_1FN;

SELECT 'TABLA EN 2FN ' AS '';
SELECT * FROM Appointments_2FN;

SELECT 'TABLAS EN 3FN (NORMALIZADAS)' AS '';
SELECT 'Patients_3FN:' AS '';
SELECT * FROM Patients_3FN;
SELECT 'Doctors_3FN:' AS '';
SELECT * FROM Doctors_3FN;
SELECT 'Appointments_3FN:' AS '';
SELECT * FROM Appointments_3FN;

SELECT 'CONSULTA EJEMPLO: Citas con Información Completa (3FN) ' AS '';
SELECT 
    a.Appointment_ID,
    p.Patient_Name,
    p.Patient_Phone,
    d.Doctor_Name,
    d.Specialty,
    a.Date,
    a.Time
FROM Appointments_3FN a
INNER JOIN Patients_3FN p ON a.Patient_ID = p.Patient_ID
INNER JOIN Doctors_3FN d ON a.Doctor_ID = d.Doctor_ID
ORDER BY a.Appointment_ID;