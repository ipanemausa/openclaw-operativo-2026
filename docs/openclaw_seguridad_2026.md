# Política de seguridad OpenClaw 2026 (borrador)

Este documento define las reglas mínimas de seguridad para usar OpenClaw en mi ecosistema local (OpenClaw + Discord + Globy).

## Principios

- Mínimo privilegio: cada integración solo tiene los permisos estrictamente necesarios.
- Nunca usar un solo token universal para todo.
- OpenClaw no puede ejecutar comandos de sistema ni tocar carpetas fuera de las explícitamente permitidas.

## Estado actual (2026-05-04)

- Globy entra a mi sistema solo vía `webhook_globy.py`, que está ligado a este repositorio.
- El webhook se ejecuta solo en localhost, no expuesto a internet.
- Aún NO está permitido que OpenClaw ejecute acciones automáticas sobre el sistema desde estas tareas; solo lectura y diseño.

(Más reglas se irán sumando en próximas sesiones.)
