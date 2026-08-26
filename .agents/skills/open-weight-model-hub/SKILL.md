---
name: open-weight-model-hub
description: Hub de Plugins e Integración Unificada de Modelos Open-Weight (DeepSeek-R1, DeepSeek-V3, Qwen 2.5, GLM-4, Kimi K3, Ollama/vLLM) inspirado en la arquitectura plug-and-play de DeepSeek Harness.
---

# 🔌 Open-Weight Model Hub & Plugin Registry (DeepSeek Standard)

Este catálogo centraliza todos los motores de lenguaje de código abierto y modelos de frontera en una arquitectura **Plug-and-Play**. Elimina la necesidad de escribir scripts ad-hoc de conexión para cada modelo.

---

## 🗂️ Registro de Plugins de Modelos Activos

| Plugin / Modelo | Tipo / Hosting | Endpoint / Protocolo | Rol Principal |
| :--- | :--- | :--- | :--- |
| **`plugin-deepseek-r1`** | Open-Weight (DeepSeek Inc.) | `POST /api/deepseek/chat` (`deepseek-reasoner`) | Razonamiento lógico profundo, matemáticas y refactorización algorítmica. |
| **`plugin-deepseek-v3`** | Open-Weight (DeepSeek Inc.) | `POST /api/deepseek/chat` (`deepseek-chat`) | Inferencia conversacional de alta velocidad y baja latencia (MoE + MLA). |
| **`plugin-qwen-2.5`** | Open-Weight (Alibaba Cloud) | Direct OpenAI-Compatible / Fireworks AI | Parseo de JSON determinista, tareas de visión-lenguaje y código. |
| **`plugin-kimi-k3`** | Serverless ZDR (Moonshot AI) | Fireworks AI / OpenRouter | Procesamiento de super-long context (hasta 1M tokens) con política ZDR. |
| **`plugin-local-ollama`** | Local Self-Hosted GPU | `http://localhost:11434/api/generate` | Inferencia 100% offline sin conexión a internet ni consumo de API externa. |

---

## ⚙️ Esquema Único de Invocación (JSON Standard)

Cualquier agente del sistema invoca cualquier modelo Open-Weight mediante el siguiente payload normalizado:

```json
{
  "plugin": "plugin-deepseek-r1",
  "agent": "bilingual_cs",
  "message": "Tu consulta de ingeniería o negocio aquí",
  "temperature": 0.7
}
```

---

## 🔒 Beneficios Operativos
1. **Sustitución Transparente de Modelos**: Se puede alternar entre `DeepSeek-R1`, `Qwen` u `Ollama` cambiando únicamente la clave `"plugin"`.
2. **Cero Fricción en Integraciones Futuras**: Cuando se lance un nuevo modelo (ej. DeepSeek-V5 o Llama-4), solo se agrega su archivo de plugin en `.agents/skills/open-weight-model-hub/` sin tocar el código fuente del frontend ni del backend.
