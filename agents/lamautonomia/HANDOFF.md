# 🤝 LAMAUTONOMIA — Protocolo de Continuidad (HANDOFF)

> Usa este documento cuando Antigravity se bloquee o deje de responder.
> Sigue los pasos en orden. No omitas ninguno.

---

## 🚨 Paso 1 — Verifica que Antigravity realmente está bloqueado

Señales de bloqueo:
- No responde después de 2 minutos
- Dice "no puedo hacer eso" repetidamente sin avanzar
- La conversación se congela o cierra

---

## 📋 Paso 2 — Abre el archivo de contexto actual

Localiza este archivo y ábrelo:
```
C:\Users\ipane\openclaw-operativo-2026\agents\lamautonomia\current_task.md
```

Copia **todo** su contenido.

---

## 🤖 Paso 3 — Abre Copilot en Edge

1. Abre Microsoft Edge
2. Haz clic en el ícono de Copilot (esquina superior derecha)
3. Selecciona el modo **"Más preciso"** o **"Equilibrado"**

---

## 📤 Paso 4 — Pega el contexto a Copilot

Pega exactamente este texto al inicio, seguido del contenido de `current_task.md`:

```
Eres el agente de continuidad del sistema LAMAUTONOMIA. 
Antigravity se bloqueó. Necesito que retomes la tarea exactamente donde se quedó.
Lee el contexto completo y confirma que entendiste antes de actuar.
NO hagas cambios hasta que yo lo confirme.

--- CONTEXTO LAMAUTONOMIA ---
[PEGAR AQUÍ EL CONTENIDO DE current_task.md]
```

---

## ✅ Paso 5 — Confirma el contexto con Copilot

Antes de que Copilot ejecute cualquier cosa, pídele que confirme:
- ¿Qué tarea va a retomar?
- ¿Qué archivos va a modificar?
- ¿Qué comandos va a ejecutar?

---

## 📝 Paso 6 — Registra el handoff en LAMAUTONOMIA

Cuando Copilot termine su tarea, registra el evento:

```powershell
cd C:\Users\ipane\openclaw-operativo-2026
.\scripts\lamautonomia-pipeline.ps1 -Servicio "handoff" -Mensaje "Copilot retomo tarea desde Antigravity: [descripcion de lo que hizo]"
```

---

## 🔄 Paso 7 — Vuelve a Antigravity cuando esté disponible

Cuando Antigravity vuelva a estar operativo:
1. Pégale el log de lo que hizo Copilot
2. Pídele que actualice `current_task.md`
3. Continúa el trabajo normal

---

## ⚡ Resumen rápido (referencia rápida)

```
Antigravity bloqueado
    ↓
Abrir: current_task.md
    ↓
Copiar contenido completo
    ↓
Abrir Copilot en Edge
    ↓
Pegar contexto + pedir confirmación
    ↓
Copilot ejecuta tarea
    ↓
Registrar en pipeline LAMAUTONOMIA
    ↓
Volver a Antigravity cuando esté disponible
```

---

## 📞 Contexto de emergencia para Copilot

Si no tienes tiempo de abrir `current_task.md`, usa este texto mínimo:

```
Copilot, soy Guillermo. Trabajo en el proyecto openclaw-cloud-2026 
(C:\Users\ipane\openclaw-cloud-2026). Tengo 5 contenedores Docker 
corriendo que NO debo interrumpir. Mi sistema de gobernanza se llama 
LAMAUTONOMIA y está en C:\Users\ipane\openclaw-operativo-2026\agents\lamautonomia\.
Necesito ayuda con: [DESCRIBE TU TAREA AQUÍ]
Regla crítica: no reinicies Docker ni modifiques docker-compose.yml sin mi confirmación.
```

---

*LAMAUTONOMIA Continuity Protocol v1.0 — 2026-06-25*
