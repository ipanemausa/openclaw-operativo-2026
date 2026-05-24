import os
import json
import requests
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

# Inicializar app Slack
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

# URL de OpenClaw MCP
MCP_URL = "http://127.0.0.1:18789"

@app.command("/oc")
def handle_oc_command(ack, command, client):
    ack()
    
    agent = command.get("text", "chat").split()[0]
    message = " ".join(command.get("text", "").split()[1:]) or "status"
    
    try:
        response = requests.post(
            f"{MCP_URL}/api/mcp/message",
            json={"agent": agent, "message": message}
        )
        result = response.json()
        
        client.chat_postMessage(
            channel=command["channel_id"],
            text=json.dumps(result, indent=2)
        )
    except Exception as e:
        client.chat_postMessage(
            channel=command["channel_id"],
            text=f"Error: {str(e)}"
        )

@app.event("app_mention")
def handle_mention(event, client):
    text = event["text"]
    client.chat_postMessage(
        channel=event["channel"],
        text=f"OpenClaw responding to: {text}"
    )

if __name__ == "__main__":
    handler = SocketModeHandler(app, os.environ.get("SLACK_APP_TOKEN"))
    handler.start()
