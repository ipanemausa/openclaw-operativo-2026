import json
import logging
from typing import Any, Dict

logger = logging.getLogger(__name__)

class MCPGateway:
    def __init__(self):
        self.context = {}
        self.agents = {}
    
    def register_agent(self, name: str, agent_config: Dict[str, Any]):
        self.agents[name] = agent_config
        logger.info(f"Agent registered: {name}")
    
    def send_message(self, agent: str, message: str, context: Dict = None) -> Dict:
        if agent not in self.agents:
            return {"error": f"Agent {agent} not found"}
        
        self.context.update(context or {})
        logger.info(f"Message to {agent}: {message}")
        
        return {
            "status": "received",
            "agent": agent,
            "message": message,
            "context": self.context
        }
    
    def get_status(self) -> Dict:
        return {
            "agents": list(self.agents.keys()),
            "context": self.context
        }

mcp = MCPGateway()
