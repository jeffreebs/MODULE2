DROP TABLE IF EXISTS automoviles_original;

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

SELECT * FROM automoviles_original;

DROP TABLE IF EXISTS automobiles ;
CREATE TABLE automobiles (
    vin TEXT PRIMARY KEY,
    make TEXT NOT NULL,
    model TEXT NOT NULL,
    year INTEGER NOT NULL,
    color TEXT
);

DROP TABLE IF EXISTS owners;
CREATE TABLE owners (
    owner_id INTEGER PRIMARY KEY,
    owner_name TEXT NOT NULL,
    owner_phone TEXT

);

DROP TABLE IF EXISTS car_owners;
CREATE TABLE car_owners (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    vin TEXT,
    owner_id INTEGER,
    insurance_policy TEXT,
    FOREIGN KEY (vin) REFERENCES automobiles (vin),
    FOREIGN KEY (owner_id) REFERENCES owners(owner_id),
    FOREIGN KEY (insurance_policy) REFERENCES insurance_policies (insurance_policy)

);

DROP TABLE IF EXISTS insurance_policies;
CREATE TABLE insurance_policies (
    insurance_policy TEXT PRIMARY KEY,
    insurance_company TEXT NOT NULL
);

INSERT INTO automobiles (vin,make, model, year, color )
SELECT DISTINCT vin, make, model, year, color
FROM automoviles_original;


INSERT INTO owners( owner_id, owner_name,owner_phone)
SELECT DISTINCT owner_id, owner_name, owner_phone
FROM automoviles_original;


INSERT INTO insurance_policies (insurance_policy, insurance_company)
SELECT DISTINCT insurance_policy, insurance_company
FROM automoviles_original;

INSERT INTO car_owners(vin, owner_id, insurance_policy)
SELECT vin , owner_id, insurance_policy
FROM automoviles_original;


SELECT * FROM automobiles;
SELECT * FROM owners;
SELECT * FROM insurance_policies;
SELECT * FROM car_owners; 



