"""
==============================================================================
OPENCLAW CORE MATRIX 2026 — TEST DE INTEGRACIÓN REAL
==============================================================================
Verifica que el AI Router conecta realmente con DeepSeek y Qwen.
Pregunta sobre HB Jewelry — respuesta real, con latencia y tokens.
==============================================================================
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from ai_router import router

PREGUNTA_HB = (
    "Eres un experto en marketing de joyería de lujo para el mercado latinoamericano. "
    "Lista exactamente 3 estrategias concretas y accionables para aumentar ventas online "
    "de HB Jewelry, una marca de joyería de alta gama. Responde directo, sin introducción."
)

SYSTEM_JEWELRY = (
    "Eres el asistente especializado de HB Jewelry. "
    "Respondes en español, con foco en mercado latinoamericano y norteamericano hispanohablante. "
    "Eres conciso, práctico y orientado a resultados de negocio reales."
)

def run_test():
    print("=" * 60)
    print("  OPENCLAW AI ROUTER — TEST DE INTEGRACIÓN REAL")
    print("  Fecha: 2026-08-22")
    print("=" * 60)

    results = []

    # Test 1: DeepSeek directo
    print("\n[TEST 1/2] DeepSeek — Código y razonamiento estructurado")
    r1 = router.call(
        prompt=PREGUNTA_HB,
        task_type="code",  # → deepseek
        system=SYSTEM_JEWELRY,
    )
    router.print_result(r1)
    results.append(("DeepSeek", r1))

    # Test 2: Qwen vía OpenRouter
    print("\n[TEST 2/2] Qwen 72B vía OpenRouter — Multilingüe / RAG / Joyería")
    r2 = router.call(
        prompt=PREGUNTA_HB,
        task_type="jewelry",  # → qwen
        system=SYSTEM_JEWELRY,
    )
    router.print_result(r2)
    results.append(("Qwen", r2))

    # Resumen
    print("\n" + "=" * 60)
    print("  RESUMEN DEL TEST")
    print("=" * 60)
    all_ok = True
    for name, r in results:
        status = "[OK] REAL" if r["success"] else "[FAIL]"
        print(f"  {status} | {name:<10} | {r['latency_ms']:>5}ms | {r['tokens']:>4} tokens")
        if not r["success"]:
            all_ok = False

    print("=" * 60)
    if all_ok:
        print("  [SUCCESS] TODOS LOS MODELOS RESPONDEN CON DATOS REALES")
        print("  No hay mocks. No hay simulaciones.")
    else:
        print("  [WARNING] Algunos modelos fallaron. Revisar keys en master.env")
    print("=" * 60)

    return all_ok


if __name__ == "__main__":
    success = run_test()
    sys.exit(0 if success else 1)
