# Integración Globy ↔ OpenClaw

**Fecha**: 2026-04-25  
**Objetivo**: Conectar Globy (agente conversacional de Perplexity) con OpenClaw para orquestar tareas automáticas desde chat.

## Flujo propuesto

1. Usuario escribe tarea en Globy
2. Globy identifica que requiere ejecución en OpenClaw
3. Globy genera payload JSON con instrucciones
4. Globy llama webhook de OpenClaw o API
5. OpenClaw ejecuta tarea y responde
6. Globy confirma al usuario

## Requisitos técnicos

- Webhook público en OpenClaw (puerto 8080 expuesto)
- Autenticación con token
- Logs de todas las llamadas
- Timeout configurado (30s max)

## Estado

- [x] Definir endpoint en OpenClaw
- [x] Configurar autenticación
- [ ] Probar desde Globy
- [ ] Documentar ejemplos de uso

## Flujo actual Globy → OpenClaw (Mayo 2026)

- **Arquitectura**: Globy llama al script `webhook_globy.py` (Flask) que actúa como receptor de tareas.
- **Payload**: El JSON mínimo esperado contiene:
  ```json
  {
    "task": "descripción de la tarea",
    "params": {}
  }
  ```
- **Acción actual**: El webhook valida el token `Bearer`, registra la petición en `logs/webhook.log` y retorna una respuesta mock (`status: executed`).
- **Restricciones**: Actualmente NO ejecuta comandos directos en OpenClaw; solo funciona como receptor y log de misiones.

---
**Prueba validada el 2026-05-04**: `webhook_globy.py` recibió correctamente tarea de prueba y quedó registrada en `logs/webhook.log`.
