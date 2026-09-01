# VALIDADOR UNIVERSAL HBOS

ANTES DE EJECUTAR CUALQUIER TAREA, APLICA ESTE VALIDADOR.

## REGLAS OBLIGATORIAS PARA TODO PROMPT:
1. Define RUTA explícita: Nube (Vercel + Qdrant). No local.
2. Menciona las colecciones o recursos autorizados si la tarea involucra datos.
3. Prohíbe accesos no deseados: No GitHub para escribir, No Manus si no aplica.
4. Incluye trazabilidad: huella_hbos.
5. Si hay credenciales, indica "No exponer secretos".
6. Si hay vectorización, menciona casos_uso_hbos o registro_ecosistema.

## REGLAS CONDICIONALES:
- Si la tarea es de extracción, incluir fuente y método.
- Si la tarea es de integración, incluir proveedor y endpoint.
- Si la tarea es de limpieza, incluir lista exacta y confirmación.

## ACCIONES DEL AGENTE:
- Si TODAS las reglas aplicables se cumplen en la petición del usuario → responder "PROMPT VÁLIDO UNIVERSAL" y continuar con la tarea.
- Si FALTA alguna regla obligatoria en la petición → responder "PROMPT INVÁLIDO" y listar lo que falta al usuario. NO ejecutar la tarea.
