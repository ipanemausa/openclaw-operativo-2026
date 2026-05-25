# Diagnóstico y Arquitectura de Hermes en OpenClaw

Este documento formaliza la integración de **Hermes** dentro del ecosistema OpenClaw 2026.5.24. Describe cómo conviven los diferentes agentes, scripts y herramientas para evitar colisiones y mantener una sincronización perfecta.

---

## 1. Mapa del Ecosistema Actual

El ecosistema actual opera bajo un esquema híbrido y distribuido:

- **PC Host (Windows):** Donde reside el código fuente (GitHub) y los archivos operativos (OneDrive, WMS Exports).
- **Docker / Gateway:** Infraestructura de contenedores y enrutamiento (MCP Gateway) que aloja herramientas y agentes.
- **Gordon & Antigravity (Gemini):** Agentes encargados de desarrollo, validación y creación de reglas (`docs/`).
- **pwsh CLI / Scripts (.ps1, .vba):** Capa de automatización de bajo nivel. Ejecuta tareas deterministas (como el pipeline de Excel o control de impresoras).
- **Operador (Washington):** Actor humano encargado de la ejecución física y resolución de excepciones en el pipeline.
- **Estado Global (`state/`):** El "cerebro de progreso". Único canal válido para la comunicación asíncrona entre agentes.

---

## 2. Puntos de Fricción Identificados y Mitigaciones

1. **Agentes improvisando rutinas o "alucinando" arquitecturas:**
   - *Mitigación:* Ningún agente actúa como pieza suelta. Todo desarrollo debe pasar por la fase de planeación (`implementation_plan.md`) y toda ejecución debe basarse en archivos `.yaml` dentro de `state/`.
2. **Colisión de lectura/escritura (Race Conditions):**
   - *Mitigación:* Regla dura "Leer primero, Actualizar después" del `state_contract.md`. Hermes orquesta, Gordon/Antigravity desarrollan, CLI/Operador ejecutan.
3. **Peligros de seguridad por permisos excesivos:**
   - *Mitigación:* Hermes y otros agentes automatizados no operan como administradores. Las operaciones que modifican la infraestructura base (Ej. impresión, conexión al WMS local) se mantienen localizadas mediante rutinas de CLI o la intervención del Operador (Washington).

---

## 3. Rol Oficial de Hermes (Orquestador / Planner)

**Hermes NO es un generador de código aislado ni un ejecutor directo.** Su rol oficial es el de **Coordinador y Enrutador de Tareas (Task Router)**.

### Flujo de Trabajo Multiagente liderado por Hermes:

1. **Iniciación:** Hermes detecta o es notificado de una nueva necesidad.
2. **Definición de Pasos:** Hermes actualiza un archivo de estado en `state/`, definiendo el mapa de `steps`. (`meta.last_actor: "hermes"`).
3. **Delegación:** 
   - Tareas de código / diseño: Gordon o Antigravity toman el estado.
   - Tareas operativas: pwsh CLI o el Operador ejecutan.
4. **Verificación:** Los agentes o actores humanos actualizan el `status` a `done` o `error`.
5. **Cierre:** Hermes lee la confirmación y marca el workflow general como completo.

---

## 4. Protocolos de Seguridad y Limitaciones

- **Acceso:** Hermes corre contenedorizado/aislado. Accede al sistema a través de herramientas MCP bien definidas, sin privilegios de root absolutos.
- **Comunicación con WMS:** Está estrictamente prohibido que Hermes interactúe directamente con la API del WMS local por razones de seguridad. Toda interacción con la logística se hace a través de exportaciones (Archivos Excel) procesados localmente.
- **Modificación Directa de Producción:** Hermes solo aprueba planes o avanza el `current_step`. La escritura de código se delega a Antigravity/Gordon y su testeo se hace en el host controlado.
