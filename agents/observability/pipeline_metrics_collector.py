# =====================================================================
# HB JEWELRY PIPELINE METRICS COLLECTOR (2026.7.1)
# =====================================================================
# Colecta métricas de ejecución, tiempos por nodo DAG y recursos Docker.
# Guarda el reporte consolidado en /public/pipeline_metrics.json
# =====================================================================

import os
import sys
import json
import time
import subprocess

print("=========================================================")
print(" [AI] RECOPILANDO MÉTRICAS DE TELEMETRÍA DEL PIPELINE ")
print("=========================================================")

MANIFEST_PATH = "C:/openclaw/hb-jewelry/public/dag_pipeline_execution_result.json"
METRICS_OUT = "C:/openclaw/hb-jewelry/public/pipeline_metrics.json"

def collect_metrics():
    node_metrics = []
    if os.path.exists(MANIFEST_PATH):
        with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            node_metrics = data.get("trace", [])

    # Verificar estado de contenedores Docker
    docker_status = "UNKNOWN"
    try:
        res = subprocess.run("docker ps --format \"{{.Names}}\"", shell=True, capture_output=True, text=True)
        containers = [c.strip() for c in res.stdout.strip().split("\n") if c.strip()]
        docker_status = f"ACTIVE ({len(containers)} containers)"
    except Exception as e:
        docker_status = f"ERROR: {e}"

    metrics_payload = {
        "system": "HB Jewelry Pipeline Observability Collector v2026.7.1",
        "timestamp": time.time(),
        "date": time.strftime("%Y-%m-%d %H:%M:%S"),
        "docker_status": docker_status,
        "total_nodes_executed": len(node_metrics),
        "nodes": node_metrics,
        "health_score": 1.0 if len(node_metrics) > 0 else 0.0
    }

    os.makedirs(os.path.dirname(METRICS_OUT), exist_ok=True)
    with open(METRICS_OUT, "w", encoding="utf-8") as f:
        json.dump(metrics_payload, f, indent=2, ensure_ascii=False)

    print(f"[OK] Métricas colectadas exitosamente en: {METRICS_OUT}")
    print("=========================================================")

if __name__ == "__main__":
    collect_metrics()
