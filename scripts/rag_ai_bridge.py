"""
==============================================================================
OPENCLAW CORE MATRIX 2026 — RAG + AI ROUTER BRIDGE
==============================================================================
Conecta el financial_rag_worker:8093 con el AI Router real.
Flujo:
  1. Query llega en lenguaje natural
  2. RAG recupera contexto relevante de Qdrant (S >= 0.82)
  3. Contexto + Query pasan por Sandbox Guardrail
  4. DeepSeek/Qwen responde con datos reales de HB Jewelry
  5. Respuesta auditada en JSONL

Uso:
  python scripts/rag_ai_bridge.py "Cuales son las joyas mas vendidas este mes?"
==============================================================================
"""

import sys
import os
import json
import requests
sys.path.insert(0, os.path.dirname(__file__))

from ai_router import router
from sandbox_guardrail import sandbox

RAG_URL = "http://localhost:8093"


def query_rag(question: str) -> dict:
    """Consulta el financial_rag_worker y retorna contexto recuperado."""
    try:
        resp = requests.post(
            f"{RAG_URL}/api/rag/query",
            json={"query": question},
            timeout=35,
        )
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.ReadTimeout:
        return {"error": "RAG timeout (>35s)", "answer": ""}
    except requests.exceptions.ConnectionError:
        return {"error": "RAG worker no disponible en :8093", "answer": ""}
    except Exception as e:
        return {"error": str(e), "answer": ""}


def rag_answer(question: str, task_type: str = "rag") -> dict:
    """
    Pipeline completo: RAG -> Sandbox -> AI Router -> Respuesta real.

    Args:
        question: Pregunta en lenguaje natural sobre HB Jewelry
        task_type: Tipo de tarea (rag, jewelry, code, etc.)

    Returns:
        dict con: answer, model, tokens, latency_ms, rag_context_used, success
    """
    print(f"\n[RAG BRIDGE] Query: {question[:80]}...")

    # Paso 1: Recuperar contexto del RAG
    print("[1/3] Consultando financial_rag_worker:8093...")
    rag_result = query_rag(question)

    if "error" in rag_result and not rag_result.get("answer"):
        rag_context = ""
        print(f"  [WARN] RAG no disponible: {rag_result['error']}")
    else:
        raw = rag_result.get("answer") or rag_result.get("context") or str(rag_result)
        rag_context = raw[:2000]
        print(f"  [OK] Contexto RAG recuperado: {len(rag_context)} chars")

    # Paso 2: Construir prompt con contexto
    system_prompt = (
        "Eres el asistente financiero y de negocios de HB Jewelry. "
        "Usas los datos de contexto proporcionados para dar respuestas precisas y accionables. "
        "Respondes en espanol, con foco en el mercado latinoamericano y norteamericano hispanohablante. "
        "Si no tienes datos suficientes, lo indicas claramente."
    )

    augmented_prompt = f"""CONTEXTO DE BASE DE DATOS HB JEWELRY:
{rag_context}

PREGUNTA DEL USUARIO:
{question}

Responde de forma concisa y practica basandote en el contexto anterior."""

    # Paso 3: Pasar por Sandbox -> AI Router
    print(f"[2/3] Enviando al AI Router via Sandbox ({task_type})...")
    result = sandbox.call(
        router=router,
        prompt=augmented_prompt,
        task_type=task_type,
        system=system_prompt,
    )

    if result.get("blocked"):
        print(f"  [BLOCKED] {result['response']}")
        return {
            "answer": result["response"],
            "model": result.get("model", "blocked"),
            "tokens": 0,
            "latency_ms": 0,
            "rag_context_used": False,
            "success": False,
        }

    print(f"[3/3] Respuesta recibida: {result['tokens']} tokens, {result['latency_ms']}ms")

    return {
        "answer": result["response"],
        "model": result["model"],
        "tokens": result["tokens"],
        "latency_ms": result["latency_ms"],
        "rag_context_used": bool(rag_context and len(rag_context) > 50),
        "success": result["success"],
    }


def print_answer(result: dict):
    """Imprime la respuesta de forma legible."""
    print(f"\n{'='*60}")
    print(f"  MODELO:   {result['model']}")
    print(f"  TOKENS:   {result['tokens']}")
    print(f"  LATENCIA: {result['latency_ms']}ms")
    print(f"  RAG:      {'Contexto real usado' if result['rag_context_used'] else 'Conocimiento general'}")
    print(f"{'='*60}")
    print(f"\n{result['answer']}\n")
    print(f"{'='*60}")


if __name__ == "__main__":
    # Pregunta por defecto o desde argumento CLI
    question = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else (
        "Cuales son las categorias de productos de HB Jewelry y que estrategia de precios recomiendas?"
    )

    result = rag_answer(question, task_type="jewelry")
    print_answer(result)
