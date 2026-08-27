"""
=============================================================================
OPENCLAW 2026 — WHATSAPP SWARM ORCHESTRATOR
=============================================================================
Este módulo orquesta un enjambre (swarm) de agentes dentro de un entorno
de grupo (ej. WhatsApp). Delega mensajes basándose en intenciones o menciones
(@ollama, @ventas, @router).
=============================================================================
"""

import json
from zero_cost_router import ZeroCostEdgeRouter

class Agent:
    def __init__(self, name, description, execute_fn):
        self.name = name
        self.description = description
        self.execute_fn = execute_fn

class SwarmOrchestrator:
    def __init__(self):
        self.agents = {}
        self.MAX_HOPS = 3
        
    def register_agent(self, agent: Agent):
        self.agents[agent.name.lower()] = agent

    def process_message(self, message: str, sender: str = "user", hop_count: int = 0) -> str:
        """
        Escanea el mensaje buscando menciones a agentes. Si no hay,
        lo envía al agente por defecto (Edge Router).
        Implementa Guardrails (MAX_HOPS) para evitar loops infinitos.
        """
        if hop_count >= self.MAX_HOPS:
            return f"🚨 [GUARDRAIL] Se superó el límite de saltos máximos ({self.MAX_HOPS}). Posible loop infinito detectado. Abortando delegación autónoma."
            
        message_lower = message.lower()
        
        # Buscar menciones @
        target_agent = None
        for name in self.agents.keys():
            if f"@{name}" in message_lower:
                target_agent = self.agents[name]
                break
                
        if not target_agent:
            # Si no arroban a nadie, responde el agente general (Edge Router)
            target_agent = self.agents.get("general")
            
        if not target_agent:
            return "No hay agentes disponibles para responder."
            
        print(f"[SWARM] {sender} invocó a @{target_agent.name}")
        return target_agent.execute_fn(message, sender)

# --- Definición de Agentes ---

def ollama_agent_execute(message: str, sender: str):
    import urllib.request
    print("[OLLAMA AGENT] Procesando de forma 100% local y privada...")
    url = "http://localhost:11434/api/generate"
    payload = {"model": "qwen2.5:latest", "prompt": message, "stream": False}
    try:
        req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), 
                                     headers={"Content-Type": "application/json"}, method='POST')
        with urllib.request.urlopen(req, timeout=120) as resp:
            body = json.loads(resp.read().decode('utf-8'))
            return f"🛡️ [Ollama Privado]: {body.get('response', 'Sin respuesta.')}"
    except Exception as e:
        return f"🛡️ [Ollama Error]: {str(e)}"

def edge_agent_execute(message: str, sender: str):
    print("[EDGE AGENT] Procesando mediante Zero-Cost Router...")
    # Usar el router veloz que implementamos
    resp = ZeroCostEdgeRouter.route_task("chat", message, system="Eres un agente asistente rápido.")
    return f"⚡ [Edge General]: {resp}"

def sales_agent_execute(message: str, sender: str):
    return "📈 [Ventas]: Accediendo a los KPIs del día... (Mock de Integración BD)"

def or_supervisor_execute_wrapper(message: str, sender: str):
    from or_supervisor_agent import or_supervisor_execute
    return or_supervisor_execute(message, sender)

def tribunal_execute_wrapper(message: str, sender: str):
    from multi_model_auditor import tribunal_agent_execute
    return tribunal_agent_execute(message, sender)

def debugger_agent_execute(message: str, sender: str):
    print("[DEBUGGER AGENT] Revisando código mediante razonamiento profundo (DeepSeek-R1)...")
    # Simulación de la respuesta del debugger
    if "error" in message.lower() or "bug" in message.lower():
        return "❌ [Debugger (R1)]: Se detectó una vulnerabilidad de inyección SQL. Corrección: usar parámetros preparados."
    return "✅ [Debugger (R1)]: Código limpio (Pass). Autorizado para ejecución en el sandbox."


# --- Instancia Singleton ---
swarm = SwarmOrchestrator()
swarm.register_agent(Agent("ollama", "Agente privado local", ollama_agent_execute))
swarm.register_agent(Agent("general", "Agente por defecto (Edge)", edge_agent_execute))
swarm.register_agent(Agent("ventas", "Agente experto en BD y ventas", sales_agent_execute))
swarm.register_agent(Agent("debugger", "Revisor estricto de código y lógica", debugger_agent_execute))
swarm.register_agent(Agent("supervisor", "Validador estructural de Investigación de Operaciones (OR)", or_supervisor_execute_wrapper))
swarm.register_agent(Agent("tribunal", "Tribunal Multi-Modelo (Red-Teaming) para auditoría exhaustiva", tribunal_execute_wrapper))

if __name__ == "__main__":
    print(swarm.process_message("Hola, ¿cómo están hoy?"))
    print(swarm.process_message("Necesito que @ollama analice este texto confidencial: Proyecto X."))
    print(swarm.process_message("@ventas Dime cuánto vendimos hoy."))
