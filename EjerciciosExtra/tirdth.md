RESUMEN: NORMALIZACIÓN DE CITAS MÉDICAS
1FN: La tabla original cumple 1FN con valores atómicos y clave primaria simple (Appointment_ID). No requiere modificaciones.
2FN: Al tener clave primaria simple (no compuesta), no existen dependencias parciales. La tabla ya está en 2FN sin necesidad de cambios.
3FN: Se crean tablas separadas eliminando dependencias transitivas:

Patients: Datos del paciente (Patient_ID, Patient_Name, Patient_Phone)
Doctors: Datos del doctor (Doctor_ID, Doctor_Name, Specialty)
Appointments: Datos de la cita referenciando paciente y doctor (Appointment_ID, Patient_ID, Doctor_ID, Date, Time)

Justificación: Los datos de pacientes (nombre y teléfono) se repetían por cada cita del mismo paciente. Los datos de doctores (nombre y especialidad) se repetían por cada cita con el mismo doctor. Al separar en tablas independientes, cada paciente y cada doctor se almacenan una sola vez, eliminando redundancia y facilitando actualizaciones. Si un paciente cambia su teléfono o un doctor cambia de especialidad, solo se actualiza un registro en lugar de múltiples citas.