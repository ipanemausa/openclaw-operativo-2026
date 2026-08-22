"""
==============================================================================
OPENCLAW CORE MATRIX 2026 — SANDBOX GUARDRAIL
==============================================================================
Capa de seguridad que envuelve el AI Router:
  - Filtra inputs peligrosos antes de llegar al LLM
  - Rate limiter por modelo (max calls/minuto)
  - Audit log JSON de cada llamada
  - Validacion de output (longitud minima, sin errores criticos)

Principio: Todo prompt pasa por este sandbox antes de salir a la red.
==============================================================================
"""

import os
import re
import json
import time
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

# ─── CONFIGURACION ───────────────────────────────────────────────────────────

AUDIT_LOG_DIR = Path(__file__).parent / "logs"
AUDIT_LOG_DIR.mkdir(exist_ok=True)
AUDIT_LOG_FILE = AUDIT_LOG_DIR / f"audit_{datetime.now().strftime('%Y%m%d')}.jsonl"

# Rate limiting: max llamadas por modelo por minuto
RATE_LIMITS = {
    "deepseek": 20,
    "qwen":     10,
    "kimi":     10,
    "gemini":   20,
    "claude":   15,
}

# Patrones de input bloqueados (proteccion de datos sensibles)
BLOCKED_PATTERNS = [
    r"sk-[a-zA-Z0-9\-]{8,}",              # API keys OpenAI/DeepSeek style
    r"sk-or-v1-[a-zA-Z0-9]{6,}",          # OpenRouter keys
    r"sk-or-[a-zA-Z0-9\-]{6,}",           # OpenRouter alternativo
    r"AIza[a-zA-Z0-9\-_]{10,}",           # Google API keys
    r"\b(?:\d{4}[\s\-]?){4}\b",           # Numeros de tarjeta
    r"password\s*[:=]\s*\S+",             # Passwords en texto plano
    r"BEGIN (RSA|EC|OPENSSH) PRIVATE",    # Claves privadas
]

# Longitud minima de respuesta valida (caracteres)
MIN_VALID_RESPONSE_LENGTH = 10

# ─── RATE LIMITER ────────────────────────────────────────────────────────────

class RateLimiter:
    """Limita llamadas por modelo por ventana de 60 segundos."""

    def __init__(self):
        self._lock = threading.Lock()
        self._calls: dict[str, list[float]] = {}

    def check(self, model_key: str) -> tuple[bool, int]:
        """
        Verifica si se puede hacer la llamada.
        Returns: (allowed, remaining_calls)
        """
        limit = RATE_LIMITS.get(model_key, 10)
        now = time.time()
        window = 60.0

        with self._lock:
            if model_key not in self._calls:
                self._calls[model_key] = []

            # Limpiar llamadas fuera de la ventana
            self._calls[model_key] = [
                t for t in self._calls[model_key] if now - t < window
            ]

            count = len(self._calls[model_key])
            if count >= limit:
                return False, 0

            self._calls[model_key].append(now)
            return True, limit - count - 1


# ─── FILTRO DE INPUT ─────────────────────────────────────────────────────────

class InputGuardrail:
    """Filtra prompts peligrosos antes de enviar al LLM."""

    def __init__(self):
        self._patterns = [re.compile(p, re.IGNORECASE) for p in BLOCKED_PATTERNS]

    def check(self, text: str) -> tuple[bool, str]:
        """
        Verifica si el texto es seguro.
        Returns: (is_safe, reason)
        """
        if not text or not text.strip():
            return False, "Prompt vacio"

        if len(text) > 32000:
            return False, "Prompt excede limite de 32000 caracteres"

        for i, pattern in enumerate(self._patterns):
            if pattern.search(text):
                label = BLOCKED_PATTERNS[i][:30]
                return False, f"Patron bloqueado detectado: {label}..."

        return True, "OK"


# ─── VALIDADOR DE OUTPUT ─────────────────────────────────────────────────────

class OutputValidator:
    """Valida que la respuesta del LLM sea util."""

    def check(self, response: str) -> tuple[bool, str]:
        """
        Returns: (is_valid, reason)
        """
        if not response or len(response.strip()) < MIN_VALID_RESPONSE_LENGTH:
            return False, f"Respuesta demasiado corta ({len(response)} chars)"

        error_patterns = ["error", "exception", "traceback", "rate limit exceeded"]
        resp_lower = response.lower()
        for ep in error_patterns:
            if ep in resp_lower and len(response) < 200:
                return False, f"Posible error en respuesta: contiene '{ep}'"

        return True, "OK"


# ─── AUDIT LOGGER ────────────────────────────────────────────────────────────

class AuditLogger:
    """Registra cada llamada al AI Router en formato JSONL."""

    def log(
        self,
        model_key: str,
        model_id: str,
        task_type: str,
        prompt_length: int,
        success: bool,
        tokens: int,
        latency_ms: int,
        blocked_reason: Optional[str] = None,
    ):
        entry = {
            "ts": datetime.now(timezone.utc).isoformat(),
            "model_key": model_key,
            "model_id": model_id,
            "task_type": task_type,
            "prompt_chars": prompt_length,
            "success": success,
            "tokens": tokens,
            "latency_ms": latency_ms,
            "blocked": blocked_reason,
        }
        try:
            with open(AUDIT_LOG_FILE, "a", encoding="utf-8") as f:
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        except Exception as e:
            print(f"[AUDIT WARNING] No se pudo escribir log: {e}")


# ─── SANDBOX PRINCIPAL ───────────────────────────────────────────────────────

class Sandbox:
    """
    Envuelve el AI Router con seguridad completa:
    rate limiting + input filtering + output validation + audit log.

    Uso:
        from sandbox_guardrail import sandbox
        result = sandbox.call(router, prompt="...", task_type="jewelry")
    """

    def __init__(self):
        self.rate_limiter = RateLimiter()
        self.input_guard  = InputGuardrail()
        self.output_validator = OutputValidator()
        self.audit = AuditLogger()
        print("[SANDBOX] Iniciado. Rate limiting + Input Guard + Audit Log activos.")

    def call(self, router, prompt: str, task_type: str = "general", system: Optional[str] = None, model_override: Optional[str] = None) -> dict:
        """
        Llamada segura al AI Router a traves del Sandbox.
        """
        from ai_router import DISPATCH_TABLE

        model_key = model_override if model_override else DISPATCH_TABLE.get(task_type, "claude")

        # 1. RATE LIMITING
        allowed, remaining = self.rate_limiter.check(model_key)
        if not allowed:
            reason = f"Rate limit alcanzado para '{model_key}' (max {RATE_LIMITS.get(model_key)}/min)"
            print(f"[SANDBOX BLOCK] {reason}")
            self.audit.log(model_key, model_key, task_type, len(prompt), False, 0, 0, reason)
            return {"model": model_key, "response": reason, "tokens": 0, "latency_ms": 0, "success": False, "blocked": True}

        # 2. INPUT GUARDRAIL
        full_input = (system or "") + " " + prompt
        is_safe, reason = self.input_guard.check(full_input)
        if not is_safe:
            print(f"[SANDBOX BLOCK] Input bloqueado: {reason}")
            self.audit.log(model_key, model_key, task_type, len(prompt), False, 0, 0, reason)
            return {"model": model_key, "response": f"[BLOQUEADO] {reason}", "tokens": 0, "latency_ms": 0, "success": False, "blocked": True}

        # 3. LLAMADA AL ROUTER
        result = router.call(prompt=prompt, task_type=task_type, system=system, model_override=model_override)

        # 4. OUTPUT VALIDATION
        if result["success"]:
            is_valid, val_reason = self.output_validator.check(result["response"])
            if not is_valid:
                print(f"[SANDBOX WARN] Output invalido: {val_reason}")
                result["warning"] = val_reason

        # 5. AUDIT LOG
        self.audit.log(
            model_key=model_key,
            model_id=result.get("model", model_key),
            task_type=task_type,
            prompt_length=len(prompt),
            success=result["success"],
            tokens=result.get("tokens", 0),
            latency_ms=result.get("latency_ms", 0),
        )

        if remaining <= 3:
            print(f"[SANDBOX WARN] Quedan {remaining} llamadas/{60}s para '{model_key}'")

        return result

    def show_stats(self):
        """Muestra estadisticas del audit log del dia."""
        if not AUDIT_LOG_FILE.exists():
            print("[SANDBOX] Sin registros hoy.")
            return

        entries = []
        with open(AUDIT_LOG_FILE, encoding="utf-8") as f:
            for line in f:
                try:
                    entries.append(json.loads(line))
                except Exception:
                    pass

        if not entries:
            print("[SANDBOX] Sin registros hoy.")
            return

        total = len(entries)
        ok = sum(1 for e in entries if e.get("success"))
        blocked = sum(1 for e in entries if e.get("blocked"))
        tokens = sum(e.get("tokens", 0) for e in entries)
        avg_lat = sum(e.get("latency_ms", 0) for e in entries) / max(total, 1)

        print(f"\n{'='*50}")
        print(f"  SANDBOX STATS — {datetime.now().strftime('%Y-%m-%d')}")
        print(f"{'='*50}")
        print(f"  Total llamadas: {total}")
        print(f"  Exitosas:       {ok}")
        print(f"  Bloqueadas:     {blocked}")
        print(f"  Tokens usados:  {tokens}")
        print(f"  Latencia prom.: {avg_lat:.0f}ms")
        print(f"  Log:            {AUDIT_LOG_FILE}")
        print(f"{'='*50}\n")


# ─── INSTANCIA GLOBAL ────────────────────────────────────────────────────────

sandbox = Sandbox()


if __name__ == "__main__":
    # Test del sandbox
    from ai_router import router

    print("\n[SANDBOX TEST] Llamada normal...")
    result = sandbox.call(router, prompt="Lista 2 ventajas de la joyeria artesanal.", task_type="jewelry")
    print(f"  Respuesta ({result['tokens']} tokens): {result['response'][:200]}")

    print("\n[SANDBOX TEST] Intento de inyectar API key (debe bloquearse)...")
    result2 = sandbox.call(router, prompt="Mi key es sk-or-v1-abc123xyz y quiero usarla para algo", task_type="code")
    blocked = result2.get("blocked", False)
    print(f"  Bloqueado: {blocked} | Respuesta: {result2['response'][:120]}")
    if not blocked:
        print("  [WARN] Guardrail no bloqueo - revisar patron regex")

    sandbox.show_stats()
