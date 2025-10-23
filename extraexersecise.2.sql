-- Ver que existan las columnas (phone, cashier_code)
PRAGMA table_info(invoices);

-- Si aún no están, agrégalas:
-- ALTER TABLE invoices ADD COLUMN phone TEXT;
-- ALTER TABLE invoices ADD COLUMN cashier_code TEXT NOT NULL DEFAULT 'N/A';

-- Actualiza algunas filas de ejemplo (ajusta IDs reales si difieren)
-- UPDATE invoices SET phone='2479-1111', cashier_code='A01' WHERE invoice_id IN (1,2,3);
-- UPDATE invoices SET phone='8888-0000', cashier_code='B07' WHERE invoice_id IN (4,5);

-- Consultas que pide el ejercicio:
SELECT * FROM invoices WHERE phone IS NULL OR phone = '';
SELECT * FROM invoices WHERE invoice_id = 5;