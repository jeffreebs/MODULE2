DROP TABLE IF EXISTS automoviles_original;
DROP TABLE IF EXISTS car_owners;
DROP TABLE IF EXISTS automobiles;
DROP TABLE IF EXISTS vehicle_details;
DROP TABLE IF EXISTS owners;
DROP TABLE IF EXISTS insurance_policies;


CREATE TABLE automoviles_original (
    vin TEXT,
    make TEXT,
    model TEXT,
    year INTEGER,
    color TEXT,
    owner_id INTEGER,
    owner_name TEXT,
    owner_phone TEXT,
    insurance_company TEXT,
    insurance_policy TEXT
);

INSERT INTO automoviles_original VALUES
('1HGCM82633A', 'Honda', 'Accord', 2003, 'Silver', 101, 'Alice', '123-456-7890', 'ABC Insurance', 'POL12345'),
('1HGCM82633A', 'Honda', 'Accord', 2003, 'Silver', 102, 'Bob', '987-654-3210', 'XYZ Insurance', 'POL54321'),
('5J6RM4H77EL', 'Honda', 'CR-V', 2014, 'Blue', 103, 'Claire', '555-123-4567', 'DEF Insurance', 'POL67890'),
('1G1RA6E11U', 'Chevrolet', 'Volt', 2015, 'Red', 104, 'Dave', '111-222-3333', 'GHI Insurance', 'POL98765');



CREATE TABLE vehicle_details (
    vehicle_id INTEGER PRIMARY KEY AUTOINCREMENT,
    make TEXT NOT NULL,
    model TEXT NOT NULL,
    year INTEGER NOT NULL
);


CREATE TABLE automobiles (
    vin TEXT PRIMARY KEY,
    vehicle_id INTEGER NOT NULL,
    color TEXT,
    FOREIGN KEY (vehicle_id) REFERENCES vehicle_details(vehicle_id)
);

CREATE TABLE owners (
    owner_id INTEGER PRIMARY KEY,
    owner_name TEXT NOT NULL,
    owner_phone TEXT
);

CREATE TABLE insurance_policies (
    insurance_policy TEXT PRIMARY KEY,
    insurance_company TEXT NOT NULL
);

CREATE TABLE car_owners (
    vin TEXT,
    owner_id INTEGER,
    insurance_policy TEXT,
    PRIMARY KEY (vin, owner_id),
    FOREIGN KEY (vin) REFERENCES automobiles(vin),
    FOREIGN KEY (owner_id) REFERENCES owners(owner_id),
    FOREIGN KEY (insurance_policy) REFERENCES insurance_policies(insurance_policy)
);



INSERT INTO vehicle_details (make, model, year)
SELECT DISTINCT make, model, year
FROM automoviles_original;


INSERT INTO automobiles (vin, vehicle_id, color)
SELECT DISTINCT 
    ao.vin,
    vd.vehicle_id,
    ao.color
FROM automoviles_original ao
INNER JOIN vehicle_details vd 
    ON ao.make = vd.make 
    AND ao.model = vd.model 
    AND ao.year = vd.year;

INSERT INTO owners (owner_id, owner_name, owner_phone)
SELECT DISTINCT owner_id, owner_name, owner_phone
FROM automoviles_original;

INSERT INTO insurance_policies (insurance_policy, insurance_company)
SELECT DISTINCT insurance_policy, insurance_company
FROM automoviles_original;

INSERT INTO car_owners (vin, owner_id, insurance_policy)
SELECT vin, owner_id, insurance_policy
FROM automoviles_original;



SELECT '=== TABLA ORIGINAL ===' AS '';
SELECT * FROM automoviles_original;

SELECT '=== VEHICLE_DETAILS (detalles únicos del vehículo) ===' AS '';
SELECT * FROM vehicle_details;

SELECT '=== AUTOMOBILES (VIN + color + referencia a vehicle_id) ===' AS '';
SELECT * FROM automobiles;

SELECT '=== OWNERS (dueños únicos) ===' AS '';
SELECT * FROM owners;

SELECT '=== INSURANCE_POLICIES (pólizas únicas) ===' AS '';
SELECT * FROM insurance_policies;

SELECT '=== CAR_OWNERS (relación N:N) ===' AS '';
SELECT * FROM car_owners;



SELECT '=== ANÁLISIS: Autos con múltiples dueños ===' AS '';
SELECT 
    a.vin,
    vd.make || ' ' || vd.model || ' ' || vd.year AS vehiculo,
    a.color,
    COUNT(DISTINCT co.owner_id) AS total_duenos,
    GROUP_CONCAT(o.owner_name, ', ') AS nombres_duenos
FROM automobiles a
INNER JOIN vehicle_details vd ON a.vehicle_id = vd.vehicle_id
INNER JOIN car_owners co ON a.vin = co.vin
INNER JOIN owners o ON co.owner_id = o.owner_id
GROUP BY a.vin, vd.make, vd.model, vd.year, a.color
HAVING COUNT(DISTINCT co.owner_id) > 1;



SELECT '=== ANÁLISIS: Dueños con múltiples autos ===' AS '';
SELECT 
    o.owner_id,
    o.owner_name,
    COUNT(DISTINCT co.vin) AS total_autos,
    GROUP_CONCAT(vd.make || ' ' || vd.model, ', ') AS autos
FROM owners o
INNER JOIN car_owners co ON o.owner_id = co.owner_id
INNER JOIN automobiles a ON co.vin = a.vin
INNER JOIN vehicle_details vd ON a.vehicle_id = vd.vehicle_id
GROUP BY o.owner_id, o.owner_name
ORDER BY total_autos DESC;



SELECT '=== CONSULTA COMPLETA: Reconstruir tabla original ===' AS '';
SELECT 
    a.vin,
    vd.make,
    vd.model,
    vd.year,
    a.color,
    o.owner_id,
    o.owner_name,
    o.owner_phone,
    ip.insurance_company,
    ip.insurance_policy
FROM automobiles a
INNER JOIN vehicle_details vd ON a.vehicle_id = vd.vehicle_id
INNER JOIN car_owners co ON a.vin = co.vin
INNER JOIN owners o ON co.owner_id = o.owner_id
INNER JOIN insurance_policies ip ON co.insurance_policy = ip.insurance_policy
ORDER BY a.vin, o.owner_id;



SELECT '=== VERIFICACIÓN: No hay duplicación de datos del vehículo ===' AS '';
SELECT 
    'Total registros en tabla original:' AS Descripcion,
    COUNT(*) AS Total
FROM automoviles_original
UNION ALL
SELECT 
    'Total VIN únicos en tabla original:',
    COUNT(DISTINCT vin)
FROM automoviles_original
UNION ALL
SELECT 
    'Total VIN en tabla automobiles:',
    COUNT(*)
FROM automobiles
UNION ALL
SELECT 
    'Total combinaciones únicas make+model+year:',
    COUNT(*)
FROM vehicle_details;