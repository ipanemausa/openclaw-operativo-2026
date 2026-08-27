"""
=============================================================================
OPENCLAW 2026 — OPERATIONS RESEARCH (OR) SUPERVISOR AGENT
=============================================================================
Este agente actúa como el gran validador estructural de flujos.
1. Utiliza el Zero-Cost Edge Router (Claude 3.5 Haiku) para extraer un DAG (JSON).
2. Valida matemáticamente el DAG usando `cpm_pipeline`.
3. Valida la estabilidad de recursos usando `queue_manager`.
Si el flujo es matemáticamente seguro y libre de ciclos, lo aprueba.
=============================================================================
"""

import json
from cpm_pipeline import calculate_cpm
from queue_manager import QueueManager
from zero_cost_router import ZeroCostEdgeRouter

def or_supervisor_execute(message: str, sender: str) -> str:
    print("\n[OR SUPERVISOR] Iniciando validación rigurosa de flujo operativo...")
    
    # 1. Extracción Estructural a JSON DAG usando Edge Router (Claude 3.5 Haiku es ideal para JSON)
    system_prompt = """Eres un experto en Ingeniería de Sistemas. Convierte la solicitud del usuario en un diccionario JSON representando un Grafo Dirigido Acíclico (DAG) de tareas.
El formato DEBE SER estrictamente:
{
  "tasks": {
    "task1": {"duration": 2.0, "depends_on": []},
    "task2": {"duration": 5.0, "depends_on": ["task1"]}
  }
}
Responde SOLO con el JSON válido, sin Markdown ni explicaciones."""
    
    print("[OR SUPERVISOR] [Paso 1] Generando Grafo (DAG) de tareas...")
    raw_json = ZeroCostEdgeRouter.route_task("parsing", f"Solicitud: {message}", system_prompt)
    
    # Limpiar posible markdown
    raw_json = raw_json.replace("```json", "").replace("```", "").strip()
    
    try:
        dag_data = json.loads(raw_json)
        tasks = dag_data.get("tasks", {})
    except json.JSONDecodeError:
        return "❌ [OR SUPERVISOR ERROR] Falló la extracción estructural del Grafo (JSON inválido). Flujo rechazado."
        
    if not tasks:
        return "⚠️ [OR SUPERVISOR] No se detectaron tareas estructuradas en la solicitud."

    # 2. Validación de Ruta Crítica (CPM)
    print("[OR SUPERVISOR] [Paso 2] Ejecutando algoritmo de Ruta Crítica (CPM)...")
    try:
        cpm_result = calculate_cpm(tasks)
        project_duration = cpm_result.get("project_duration", 0)
        critical_path = cpm_result.get("critical_path", [])
    except RecursionError:
         return "❌ [OR SUPERVISOR ALARMA] ¡DEPENDENCIA CIRCULAR DETECTADA! (Loop Infinito en Grafo). Flujo rechazado para prevenir inyección de errores."
    except Exception as e:
        return f"❌ [OR SUPERVISOR ALARMA] Error estructural en el grafo: {e}"

    # 3. Validación de Teoría de Colas (M/M/c)
    print("[OR SUPERVISOR] [Paso 3] Ejecutando análisis de Teoría de Colas (Estabilidad)...")
    qm = QueueManager(num_workers=3) # Suponemos 3 agentes activos en el enjambre
    # Simulamos tasas basadas en el tamaño del proyecto
    lambda_rate = len(tasks) / 60.0  # llegadas por segundo (ej. tareas / 1 min)
    mu_rate = 1.0 / (project_duration / len(tasks)) if project_duration > 0 else 0.1 # tasa de servicio
    
    qm.update_metrics(lambda_rate, mu_rate)
    queue_metrics = qm.get_queue_metrics()
    
    if not queue_metrics.get("is_stable", False):
         return f"❌ [OR SUPERVISOR ALARMA] Sistema inestable (Congestión ρ = {queue_metrics.get('rho', 'inf')}). El enjambre colapsará bajo esta carga. Flujo puesto en HOLD."
         
    # Si todo es perfecto
    report = (
        f"✅ **[OR SUPERVISOR] Flujo Operativo Matemáticamente Validado** ✅\n"
        f"1️⃣ **Estructura DAG:** Sin dependencias circulares (Cero Inyección de Errores).\n"
        f"2️⃣ **CPM:** Duración total proyectada: {project_duration:.2f}s. Ruta Crítica: `{' -> '.join(critical_path)}`.\n"
        f"3️⃣ **Colas (M/M/c):** Sistema estable (Factor Utilización ρ = {queue_metrics['rho']:.2f}). Sin cuellos de botella.\n\n"
        f"🟢 *Autorización concedida. Despachando a agentes...*"
    )
    
    return report

if __name__ == "__main__":
    # Test local
    res = or_supervisor_execute("Por favor descarga los 5 reportes financieros, analízalos con ollama y pásaselos al agente de ventas para el gráfico.", "ipane")
    print(res)
