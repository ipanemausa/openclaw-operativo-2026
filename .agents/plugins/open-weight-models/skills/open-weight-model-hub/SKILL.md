---
name: open-weight-model-hub
description: Hub de Plugins e Integración Unificada de Modelos Open-Weight y Herramientas Locales. Versión 2.1 — Groq (ultra-rápido) + OpenRouter (Qwen 3.8, Kimi K2, Minimax, Gemini 2.0) + DeepSeek directo + Ollama local para Antigravity IDE.
---

# 🔌 Open-Weight & Local AI Ecosystem Hub v2.1

Ecosistema completo de modelos IA: 3 tiers de velocidad + local offline.

## 🏎️ TIER 1 — GROQ: ULTRA-RÁPIDO (~1800 tok/s, gratis 600K/día)

| Tool | Modelo | Uso ideal |
|---|---|---|
| `query_groq_fast` | Llama 3.3 70B | Chat, resumen, tareas generales |
| `query_groq_coder` | Qwen 2.5 Coder 32B | Código Python/TypeScript rápido |
| `query_groq_reason` | DeepSeek R1 Distill 70B | Razonamiento sin latencia DeepSeek |

> **Key requerida:** `GROQ_API_KEY` — registro gratis en https://console.groq.com

## 🌐 TIER 2 — OPENROUTER HUB: Modelos Chinos + Gemini

| Tool | Modelo | Uso ideal |
|---|---|---|
| `query_qwen3_max` | Qwen 3.8 Max 235B | RAG, multilingüe, código, #1 benchmarks |
| `query_kimi` | Kimi K2 (1M ctx) | Documentos extensos, análisis multi-paso |
| `query_minimax` | Minimax-01 | Guiones video, análisis multimedia |
| `query_gemini_free` | Gemini 2.0 Flash | Razonamiento general, Firebase |
| `query_qwen_2_5` | Qwen 2.5 72B | Legacy, compatibilidad anterior |
| `query_orca_model` | Orca 2 13B / Mini | Razonamiento paso a paso explicativo |

> **Key ya configurada:** `OPENROUTER_API_KEY` ✅

## 🎯 TIER 3 — DEEPSEEK DIRECTO (API nativa)

| Tool | Modelo | Uso ideal |
|---|---|---|
| `query_deepseek_r1` | deepseek-reasoner | Razonamiento profundo + chain-of-thought |
| `query_deepseek_v3` | deepseek-chat | Código MoE rápido |
| `query_deepseek_harness_v4_v5` | R1/V3 + orquestación | Suite completa Harness V4/V5 |

## 💻 LOCAL — OFFLINE PRIVADO (cero datos a la nube)

| Tool | Endpoint | Modelos |
|---|---|---|
| `query_local_ollama` | localhost:11434 | qwen2.5, llama3, deepseek-r1, mistral |
| `query_lm_studio` | localhost:1234 | Cualquier GGUF local |
| `query_jan_ai` | localhost:1337 | Suite Jan AI |
| `query_anything_llm` | localhost:3001 | RAG vectorial sobre documentos locales |
| `trigger_comfyui_workflow` | localhost:8188 | Imagen/Video: Minimax H3, SDXL, WAN |

## 🎯 Regla de Despacho por Tarea

```
Tarea                 → Modelo recomendado
───────────────────────────────────────────
chat / resumen        → query_groq_fast
código rápido         → query_groq_coder
razonamiento rápido   → query_groq_reason
RAG / multilingüe     → query_qwen3_max
documentos largos     → query_kimi
guiones video         → query_minimax
razonamiento gral     → query_gemini_free
código profundo       → query_deepseek_v3
math / chain-thought  → query_deepseek_r1
privacidad total      → query_local_ollama
imagen/video local    → trigger_comfyui_workflow
```

## 🔑 Keys requeridas (en `.openclaw-master.env`)

```
OPENROUTER_API_KEY  ✅ ACTIVA
DEEPSEEK_API_KEY    ✅ ACTIVA
GEMINI_API_KEY      ✅ ACTIVA
ELEVENLABS_API_KEY  ✅ ACTIVA
GROQ_API_KEY        ⚠️  PENDIENTE → console.groq.com (gratis)
DASHSCOPE_API_KEY   ⚠️  PENDIENTE → para Qwen Image 3.0 + Qwen3-TTS
```
