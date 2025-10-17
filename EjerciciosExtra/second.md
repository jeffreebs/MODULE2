1FN: La tabla original cumple 1FN con valores atómicos y clave primaria (Student_ID, Course_Code). No requiere modificaciones.
2FN: Se separa en 3 tablas eliminando dependencias parciales:

Students: Datos del estudiante (Student_ID, Student_Name)
Courses: Datos del curso e instructor (Course_Code, Course_Name, Instructor_Name, Instructor_Email)
Enrollments: Relación estudiante-curso (Student_ID, Course_Code)


3FN: Se crea tabla Instructors eliminando dependencia transitiva donde Instructor_Email dependía de Instructor_Name:

Students: Sin cambios
Instructors: Datos del instructor (Instructor_ID, Instructor_Name, Instructor_Email)
Courses: Ahora referencia Instructor_ID en lugar de almacenar datos del instructor
Enrollments: Sin cambios
Justificación: De 1FN a 2FN eliminamos redundancia de datos de estudiantes y cursos repetidos. De 2FN a 3FN eliminamos la dependencia transitiva del email del instructor, permitiendo que un instructor con múltiples cursos tenga sus datos almacenados una sola vez y facilitando actualizaciones sin inconsistencias.