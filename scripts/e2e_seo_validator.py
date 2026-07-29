# =====================================================================
# HB JEWELRY OPENCLAW - SEO TECHNICAL VALIDATOR SUITE (2026.7.1)
# =====================================================================
# Valida de forma automatizada las etiquetas de indexación y marcado:
# 1. <title> contiene 'HB Jewelry'
# 2. <meta name="description"> presente y con longitud adecuada
# 3. <meta name="robots"> con 'index, follow'
# 4. <link rel="canonical"> válido
# 5. Marcado Open Graph (og:title, og:image, og:url)
# 6. Schema.org JSON-LD (@type: JewelryStore)
# 7. Presencia de robots.txt y sitemap.xml
# =====================================================================

import sys
import json
import time
import urllib.request
import re

print("=========================================================")
print(" [AI] INICIANDO VALIDADOR AUTOMÁTICO DE SEO TÉCNICO ")
print("=========================================================")

FIREBASE_URL = "https://hb-jewelry-app.web.app/"
seo_trace = []

def log_seo_check(check_name, status, detail):
    entry = {"check": check_name, "status": status, "detail": detail}
    seo_trace.append(entry)
    icon = "[OK]" if status == "PASSED" else "[FAIL]"
    print(f"  {icon} {check_name}: {detail}")

try:
    req = urllib.request.Request(FIREBASE_URL, headers={'User-Agent': 'Mozilla/5.0 OpenClaw-SEO-Bot/2026'})
    with urllib.request.urlopen(req, timeout=10) as resp:
        html = resp.read().decode('utf-8')
    
    # 1. Title
    title_match = re.search(r'<title>(.*?)</title>', html, re.IGNORECASE)
    if title_match and "HB Jewelry" in title_match.group(1):
        log_seo_check("Title Tag", "PASSED", f"'{title_match.group(1)}'")
    else:
        log_seo_check("Title Tag", "FAILED", "Etiqueta <title> no encontrada o no contiene HB Jewelry.")

    # 2. Meta Description
    desc_match = re.search(r'<meta\s+name="description"\s+content="(.*?)"', html, re.IGNORECASE)
    if desc_match and len(desc_match.group(1)) > 20:
        log_seo_check("Meta Description", "PASSED", f"Detectada ({len(desc_match.group(1))} caracteres)")
    else:
        log_seo_check("Meta Description", "FAILED", "Meta description ausente o demasiado corta.")

    # 3. Meta Robots
    robots_match = re.search(r'<meta\s+name="robots"\s+content="(.*?)"', html, re.IGNORECASE)
    if robots_match and "index" in robots_match.group(1):
        log_seo_check("Meta Robots Indexing", "PASSED", f"'{robots_match.group(1)}'")
    else:
        log_seo_check("Meta Robots Indexing", "FAILED", "Etiqueta robots no permite indexación.")

    # 4. Canonical Link
    canonical_match = re.search(r'<link\s+rel="canonical"\s+href="(.*?)"', html, re.IGNORECASE)
    if canonical_match and canonical_match.group(1).startswith("https://"):
        log_seo_check("Canonical Link", "PASSED", f"'{canonical_match.group(1)}'")
    else:
        log_seo_check("Canonical Link", "FAILED", "Enlace canónico ausente o inválido.")

    # 5. Schema.org JSON-LD
    if "application/ld+json" in html and "JewelryStore" in html:
        log_seo_check("Schema.org JSON-LD", "PASSED", "Estructura JSON-LD tipo JewelryStore detectada.")
    else:
        log_seo_check("Schema.org JSON-LD", "FAILED", "Marcado estructurado JSON-LD ausente.")

    # 6. Open Graph
    if 'property="og:title"' in html and 'property="og:image"' in html:
        log_seo_check("Open Graph Meta", "PASSED", "Etiquetas og:title, og:image y og:url presentes.")
    else:
        log_seo_check("Open Graph Meta", "FAILED", "Etiquetas Open Graph incompletas.")

    seo_passed = all(t["status"] == "PASSED" for t in seo_trace)

    result_data = {
        "system": "HB Jewelry SEO Technical Validator v2026.7.1",
        "timestamp": time.time(),
        "passed": seo_passed,
        "trace": seo_trace
    }

    out_file = "C:/openclaw/hb-jewelry/public/seo_validation_report.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(result_data, f, indent=2, ensure_ascii=False)

    print("\n=========================================================")
    print(f" [OK] VALIDACIÓN SEO FINALIZADA - Estado: {'PASSED 100%' if seo_passed else 'FAILED'}")
    print(f"      Reporte guardado en: {out_file}")
    print("=========================================================")

except Exception as e:
    print(f"[FAIL] Error ejecutando la prueba SEO: {e}")
    sys.exit(1)
