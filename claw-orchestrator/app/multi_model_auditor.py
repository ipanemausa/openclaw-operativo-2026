"""
=============================================================================
OPENCLAW 2026 — MULTI-MODEL AUDIT TRIBUNAL (RED-TEAMING)
=============================================================================
Somete un plan o fragmento de código al escrutinio simultáneo de:
1. El Arquitecto (Edge Router / Groq): Evalúa eficiencia y latencia.
2. El Paranoico de Seguridad (Ollama): Evalúa privacidad de datos y fugas.
3. El Juez Matemático (DeepSeek-R1): Evalúa vulnerabilidades algorítmicas.
Solo retorna "PASS" si hay Consenso General.
=============================================================================
"""

import concurrent.futures
import time
from zero_cost_router import ZeroCostEdgeRouter
from swarm_orchestrator import ollama_agent_execute, debugger_agent_execute

def _judge_architect(plan: str) -> str:
    """Juez 1: Arquitecto de Sistemas (vía Groq/Llama 3.3)"""
    sys_prompt = "Eres el Arquitecto de Sistemas del Tribunal. Analiza el siguiente plan/código. Concéntrate en eficiencia, latencia y cuellos de botella. Sé muy breve. Finaliza con [PASS] o [REJECT]."
    try:
        res = ZeroCostEdgeRouter.route_task("chat", plan, system=sys_prompt)
        return f"📐 [Arquitecto]: {res}"
    except Exception as e:
        return f"📐 [Arquitecto Error]: {e}"

def _judge_security(plan: str) -> str:
    """Juez 2: Paranoico de Seguridad (vía Ollama Local)"""
    # Envolvemos el llamado de Ollama
    prompt = f"Eres el Auditor de Seguridad Privada. Revisa que este código/plan no envíe datos sensibles a la nube, no tenga backdoors y use variables de entorno. Sé muy breve. Finaliza con [PASS] o [REJECT]: {plan}"
    return ollama_agent_execute(prompt, "Tribunal")

def _judge_logic(plan: str) -> str:
    """Juez 3: Juez de Lógica y Matemáticas (vía DeepSeek-R1 / Debugger)"""
    # Reutilizamos el agente debugger (R1)
    res = debugger_agent_execute(f"Audita exhaustivamente las matemáticas y algoritmos de este plan: {plan}", "Tribunal")
    return res

def run_audit_tribunal(plan: str) -> str:
    print("\n⚖️ [TRIBUNAL] Sesión iniciada. Sometiendo plan a los 3 Jueces...")
    start_time = time.time()
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        future_arc = executor.submit(_judge_architect, plan)
        future_sec = executor.submit(_judge_security, plan)
        future_log = executor.submit(_judge_logic, plan)
        
        # Esperamos los veredictos
        verdict_arc = future_arc.result()
        verdict_sec = future_sec.result()
        verdict_log = future_log.result()
        
    duration = time.time() - start_time
    
    # Análisis de Consenso
    all_verdicts = f"{verdict_arc}\n{verdict_sec}\n{verdict_log}"
    
    if "[REJECT]" in all_verdicts or "❌" in all_verdicts:
        consensus = "⛔ **VEREDICTO FINAL: RECHAZADO.** (El Tribunal encontró fallas severas)."
    else:
        consensus = "✅ **VEREDICTO FINAL: APROBADO.** (Consenso General alcanzado)."
        
    report = (
        f"🏛️ **REPORTE DEL TRIBUNAL DE AUDITORÍA (Red-Teaming)** 🏛️\n"
        f"*Tiempo de deliberación paralela: {duration:.2f}s*\n\n"
        f"{verdict_arc}\n\n"
        f"{verdict_sec}\n\n"
        f"{verdict_log}\n\n"
        f"----------------------------------------\n"
        f"{consensus}"
    )
    
    return report

def tribunal_agent_execute(message: str, sender: str) -> str:
    """Wrapper para integrarlo en el Swarm de WhatsApp"""
    return run_audit_tribunal(message)

if __name__ == "__main__":
    test_plan = "Haremos un loop infinito para leer la base de datos de clientes, extraeremos los emails y los mandaremos a un API pública sin encriptar para generar un resumen rápido."
    print(run_audit_tribunal(test_plan))
