# Contrato de estado compartido (`/state/*.yaml`)

Este documento define el contrato que deben respetar **todos** los agentes, scripts y personas que lean o modifiquen archivos de estado en la carpeta `state/`.

La idea central es que los archivos de estado actúan como el **cerebro de progreso** de cada loop o tarea clave.  
Si todos respetan este contrato, cualquier agente puede continuar el trabajo donde lo dejó el anterior, sin perder contexto.

---

## 1. Alcance del contrato

- Aplica a todos los archivos de la carpeta `state/` con extensión `.yaml`.
- Cada archivo representa **un loop o tarea clave**, por ejemplo:
  - `state/email_starred_loop.yaml`
  - `state/discord_notifications_loop.yaml`
  - `state/daily_review_loop.yaml`
- El contrato es obligatorio para:
  - Agentes (OC, Manus, Copilot, futuros).
  - Scripts de PowerShell u otros lenguajes.
  - Cambios manuales hechos por el usuario.

---

## 2. Estructura mínima obligatoria

Cada archivo de estado **debe** contener, como mínimo, las siguientes claves de primer nivel:

```yaml
task_id: string
title: string
status: string              # pending | in_progress | done | error
current_step: integer
steps:                      # mapa ordenado de pasos
  <numero>: string
outputs:                    # mapa de salidas relevantes
  <clave>: <valor>
meta:
  last_actor: string        # hermes | manus | oc | ps_script | manual | operator_washington | otro
  last_update: string       # ISO 8601, ej. 2026-05-01T06:45:00
```

### 2.1. `task_id`

- Identificador único y estable de la tarea/loop.
- Debe coincidir con el nombre lógico del archivo (sin ruta ni extensión) cuando sea posible.
  - Ejemplo: archivo `state/email_starred_loop.yaml` → `task_id: email_starred_loop`

### 2.2. `title`

- Descripción corta, legible por humanos, del objetivo del loop.
  - Ejemplo: `"Revisar correos importantes y generar resumen diario"`

### 2.3. `status`

Valores permitidos:

- `pending`: la tarea está definida pero aún no ha comenzado.
- `in_progress`: hay pasos en ejecución o a medio terminar.
- `done`: el loop o tarea terminó correctamente.
- `error`: la ejecución falló y requiere intervención humana o revisión.

Reglas:

- Ningún agente debe inventar otros valores de `status`.
- Para marcar `done` o `error` se recomienda añadir detalle en `outputs` o en un log externo.

### 2.4. `current_step`

- Número entero que representa el **siguiente paso a ejecutar** o el paso actualmente en proceso.
- Debe corresponder a una clave existente dentro de `steps`.
- Cuando `status` sea `done`, `current_step` puede quedarse en el último paso ejecutado.

### 2.5. `steps`

- Mapa (clave numérica → descripción de paso) que define el flujo de trabajo esperado.

Ejemplo:

```yaml
steps:
  1: "Leer configuración y conectarse a Gmail"
  2: "Obtener correos marcados con estrella de las últimas 24h"
  3: "Resumir cada hilo en 3 bullets"
  4: "Generar digest markdown y guardar ruta en output_file"
```

Reglas:

- Las claves deben ser enteros positivos (1, 2, 3, …).
- La descripción debe ser clara y orientada a acción.
- Si un agente necesita cambiar la estructura de pasos, debe:
  - Explicarlo en el commit o en un comentario.
  - Mantener la coherencia con `current_step` y `status`.

### 2.6. `outputs`

- Mapa de salidas relevantes para otros procesos o para el usuario.

Ejemplos:

```yaml
outputs:
  output_file: "outputs/digests/2026-05-01.md"
  total_threads: 7
  last_run_ok: true
```

Reglas:

- No guardar secretos ni tokens en `outputs`.
- Usar claves estables para que otros scripts puedan leerlas de forma determinista.

### 2.7. `meta`

Campos mínimos recomendados:

- `last_actor`: quién fue el último en modificar el estado.
  - Valores típicos: `hermes`, `manus`, `oc`, `ps_script`, `manual`, `operator_washington`.
- `last_update`: fecha/hora en formato ISO 8601.
  - Ejemplo: `"2026-05-01T06:45:00"`

Se pueden añadir campos adicionales según necesidad, por ejemplo:

```yaml
meta:
  last_actor: "ps_script"
  last_update: "2026-05-01T06:45:00"
  last_error: null
  notes: "Ejecutado en Azure VM"
```

---

## 3. Regla dura: leer primero, actualizar después

Cualquier agente, script o humano que quiera trabajar sobre una tarea **debe seguir este protocolo**:

1. **Leer primero** el archivo de estado completo (`state/<task>.yaml`).
2. **Decidir la acción** en función de:
   - `status`
   - `current_step`
   - `steps`
   - `outputs`
   - `meta`
3. **Ejecutar la acción** (script, llamada a API, generación de resumen, etc.).
4. **Actualizar el archivo de estado** al terminar, modificando al menos:
   - `status`
   - `current_step`
   - `outputs` (si aplica)
   - `meta.last_actor`
   - `meta.last_update`

Ejemplo de actualización típica tras completar un paso:

```yaml
status: in_progress
current_step: 3
outputs:
  output_file: "outputs/digests/2026-05-01.md"
meta:
  last_actor: "ps_script"
  last_update: "2026-05-01T06:45:00"
```

---

## 4. Reglas de concurrencia (evitar pisar cambios)

Para minimizar conflictos cuando varios agentes puedan tocar el mismo archivo:

- Preferir que **solo un agente/script** esté autorizado a ejecutar un loop concreto a la vez.
- Si se ejecutan en paralelo, aplicar estas reglas:
  - Volver a leer el archivo **justo antes** de escribir cambios.
  - Comprobar que `last_update` no ha cambiado desde que se leyó inicialmente.
  - En caso de duda, abortar la escritura y requerir intervención humana.

Una estrategia simple es que cada loop tenga un “ejecutor principal” (por ejemplo, un script PWSH). **Hermes** actuará como orquestador, definiendo y agregando pasos de alto nivel en `steps`, pero no ejecutará rutinas de bajo nivel; los demás agentes (como Gordon o Antigravity) ejecutarán esos pasos y actualizarán el `status`.

---

## 5. Errores y recuperación

Cuando una ejecución falle de forma relevante:

- Establecer `status: error`.
- Mantener `current_step` en el paso donde falló.
- Añadir información en `meta.last_error` o en un log asociado.

Ejemplo:

```yaml
status: error
current_step: 2
meta:
  last_actor: "ps_script"
  last_update: "2026-05-01T06:50:00"
  last_error: "Timeout al conectarse a la API de Gmail"
```

Recuperación:

- Un agente humano o automatizado revisa el error.
- Se corrige la causa (configuración, permisos, etc.).
- Se puede:
  - Reintentar el mismo `current_step`, o
  - Avanzar manualmente el `current_step` si corresponde.
- Se vuelve a poner `status: in_progress` antes de reanudar.

---

## 6. Extensiones del contrato

Este contrato define la **base mínima** que todos deben respetar.  
Se pueden añadir campos adicionales según el tipo de loop, por ejemplo:

- `config`: parámetros específicos (rutas, filtros, credenciales indirectas).
- `history`: lista de ejecuciones previas con timestamps.
- `links`: URLs relevantes (docs, dashboards, etc.).

Ejemplo de extensión:

```yaml
config:
  gmail_label: "STARRED"
  lookback_hours: 24

history:
  - run_at: "2026-04-30T13:00:00"
    status: "done"
    total_threads: 5
```

Reglas para extensiones:

- No romper ni renombrar las claves base (`task_id`, `title`, `status`, `current_step`, `steps`, `outputs`, `meta`).
- Documentar extensiones específicas en otros archivos de docs (`AGENT_SYSTEM.md`, docs por loop, etc.).

---

## 7. Buenas prácticas

- Tratar cada archivo de `state/` como un recurso crítico (similar a un archivo de estado de Terraform o a un workflow guardado).
- Hacer commits frecuentes cuando cambien estructura de `steps` o campos importantes de `config`.
- Mantener los archivos legibles para humanos: comentarios claros, descripciones de pasos que cualquiera pueda entender.
- Evitar guardar datos sensibles directamente; usar referencias a otros sistemas seguros cuando haga falta.
