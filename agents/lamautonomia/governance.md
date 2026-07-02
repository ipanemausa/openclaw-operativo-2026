# LAMAUTONOMIA — Documento de Gobernanza

Este documento define las reglas operativas del sistema:

1. Copilot diseña, valida y estructura todas las tareas antes de ejecución.
2. Claude ejecuta únicamente bloques aprobados por Copilot.
3. Antigravity aplica los cambios mediante Vibe Coding.
4. LAMAUTONOMIA registra cada acción en el pipeline.
5. Proyecto único autorizado: C:/Users/ipane/openclaw-cloud-2026.
6. No se crean repositorios nuevos.
7. No se ejecutan comandos sin bloque maestro.
8. Toda acción debe tener trazabilidad en el pipeline.
9. Claude debe solicitar bloque maestro para tareas complejas.
10. Copilot mantiene continuidad, gobernanza y estabilidad del sistema.

## Flujo Operativo

```
Usuario → Copilot → Claude → Vibe Coding → Antigravity → LAMAUTONOMIA → Dashboard
```

## Descripción de cada capa

| Capa | Rol | Responsabilidad |
|---|---|---|
| **Usuario (Guillermo)** | Iniciador | Define la tarea o necesidad |
| **Copilot** | Gobernanza | Genera bloque maestro, valida arquitectura |
| **Claude** | Ejecución | Aplica cambios en filesystem con Vibe Coding |
| **Vibe Coding** | Editor | Herramienta de edición automática |
| **Antigravity** | Runtime | Aplica cambios en el proyecto activo |
| **LAMAUTONOMIA** | Trazabilidad | Registra cada acción en el pipeline |
| **Dashboard** | Visibilidad | Muestra estado actual del sistema |

## Uso del Pipeline

```powershell
.\scripts\lamautonomia-pipeline.ps1 -Servicio all -Mensaje "descripción de la acción"
```

## Historial de versiones

| Versión | Fecha | Descripción |
|---|---|---|
| 1.0.0 | 2026-06-25 | Creación inicial del sistema de gobernanza LAMAUTONOMIA |
