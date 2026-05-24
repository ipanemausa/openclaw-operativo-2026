import os
import json
import requests
import threading
import time
from flask import Flask, jsonify

app_flask = Flask(__name__)

@app_flask.route('/health')
def health():
    return jsonify({"status": "ok", "message": "Mock Slack Bot is running"})

def run_flask():
    # Run the flask server on port 3000
    app_flask.run(host="0.0.0.0", port=3000)

if __name__ == "__main__":
    bot_token = os.environ.get("SLACK_BOT_TOKEN", "")
    app_token = os.environ.get("SLACK_APP_TOKEN", "")
    
    # Iniciar health check en background
    threading.Thread(target=run_flask, daemon=True).start()

    if "test-token" in bot_token or "test-token" in app_token:
        print("Running in MOCK mode with test tokens. SocketMode connection skipped.")
        while True:
            time.sleep(60)
    else:
        from slack_bolt import App
        from slack_bolt.adapter.socket_mode import SocketModeHandler
        
        # Inicializar app Slack
        app = App(token=bot_token)

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

        handler = SocketModeHandler(app, app_token)
        handler.start()

