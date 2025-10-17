1- Normalización de Empleados y Proyectos

Problemas:

- Ana Rivera aparece 2 veces (redundancia)
- Si cambio el teléfono de IT, debo cambiarlo en 2 lugares
- Mezcla datos de empleados, departamentos y proyectos


Primer paso: Llevar a Primera Forma Normal (1FN)

En este caso ya se encuentra en 1FN porque:
- Cada celda ya tiene un solo valor
- Porque no hay columnas que tengan multiples valores
- Se logra identificar cada fila


SEGUNDO PASO, LLEVAR A 2FN

ProblemaS,  hay dependencias parciales

Datos del empleado dependen SOLO de Employee ID
Datos del proyecto dependen SOLO de Project ID

La solución es separar en 3 tablas

Tabla Employees (datos que dependen de Employee ID)
Tabla Projects (datos que dependen de Project ID)
Tabla Employee_Projects (la relación entre ambos)

 Para llegar a 2FN, debemos separar la tabla eliminando las dependencias parciales.



El tercer paso es llevar a Tercera Forma Normal (3FN)

El problema es: 

-Department Phone NO depende directamente de Employee ID.
-Depende de Department:

-Employee ID → Department → Department Phone

-Esto es una dependencia transitiva.


La solución sería crear una tabla Departments
- Separar los datos del departamento en su propia tabla.




TABLAS INTERMEDIAS (1FN, 2FN, 3FN)
1FN: La tabla original ya cumple 1FN con valores atómicos y clave primaria (Employee_ID, Project_ID). No requiere cambios.
2FN: Se separa en 3 tablas para eliminar dependencias parciales:

Employees_2FN: Datos de empleados (Employee_ID, Employee_Name, Department, Department_Phone)
Projects_2FN: Datos de proyectos (Project_ID, Project_Name, Project_Budget)
Employee_Projects_2FN: Relación muchos a muchos (Employee_ID, Project_ID)

3FN: Se crea una 4ta tabla para eliminar dependencias transitivas:

Departments_3FN: Datos de departamentos (Department_ID, Department_Name, Department_Phone)
Employees_3FN: Ahora referencia Department_ID en lugar de almacenar datos del departamento
Projects_3FN: Sin cambios respecto a 2FN
Employee_Projects_3FN: Sin cambios respecto a 2FN


JUSTIFICACIÓN DE CAMBIOS
1FN a 2FN: Eliminamos redundancia y dependencias parciales. En la tabla original, los datos de empleados y proyectos se duplicaban. Al separarlos, cada dato se almacena una sola vez, evitando inconsistencias al actualizar y facilitando inserción/eliminación de registros independientes.
2FN a 3FN: Eliminamos la dependencia transitiva donde Department_Phone dependía de Department y no directamente de Employee_ID. Creando la tabla Departments, el teléfono se guarda una sola vez por departamento, reduciendo redundancia y asegurando que cambios en datos departamentales requieran actualizar solo una fila en lugar de múltiples filas de empleados.

