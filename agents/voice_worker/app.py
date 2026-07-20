import asyncio
import os
import json
import websockets
from google import genai

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("WARNING: GEMINI_API_KEY is not set.")

client = genai.Client(api_key=api_key)

async def gemini_session_handler(websocket):
    print("Client connected to Voice Worker.")
    
    # We use gemini-2.0-flash-exp as it is optimized for the Multimodal Live API
    # Gemini 1.5 Pro can also be used if configured, but 2.0-flash-exp is the default live model
    model_name = "gemini-2.0-flash-exp" 
    
    try:
        async with client.aio.live.connect(model=model_name) as session:
            print("Connected to Google Gemini Live API")
            
            # Send initial system instruction to act as an omnilingual sales and interview proxy
            await session.send(
                input="Act as an autonomous omnilingual proxy for me (the Software Architect). I am participating in technical interviews AND selling B2B IT architecture services. If the person speaks to you in English, respond in English. If they speak in Spanish, respond in Spanish. Use this strictly defined context about me: I developed complex full-stack apps like Muncher (financial module) and Teso. I specialize in AI (Copilot, RAG with Qdrant and Redis) and highly optimized architectures using Operations Research (e.g. Edge Computing and Web Audio API to bypass backend latency). My stack is Docker Compose, NGINX, React/Vite, Python/FastAPI, and PostgreSQL. Do not act like a translator, act like ME answering them directly. Maintain a highly professional, confident, and senior tone. If they are interested in my services, tell them we can schedule a meeting to analyze their infrastructure.",
                end_of_turn=True
            )

            async def receive_from_client():
                async for message in websocket:
                    if isinstance(message, bytes):
                        # Assuming raw PCM audio chunks from browser (needs specific sample rate)
                        # The client must send audio in a format supported by Gemini
                        await session.send(input={"data": message, "mime_type": "audio/pcm;rate=16000"}, end_of_turn=True)
                    elif isinstance(message, str):
                        try:
                            data = json.loads(message)
                            if data.get('type') == 'text':
                                await session.send(input=data['text'], end_of_turn=True)
                        except json.JSONDecodeError:
                            pass

            async def receive_from_gemini():
                async for response in session.receive():
                    # Gemini streams back audio chunks
                    if response.data:
                        # Send binary audio directly back to the frontend
                        await websocket.send(response.data)
                        # Send binary audio directly back to the frontend
                        await websocket.send(response.data)

                    
                    if response.text:
                        print(f"Gemini Translation: {response.text}")
                        # Optional: Send text transcription back to frontend
                        await websocket.send(json.dumps({"type": "transcription", "text": response.text}))

            await asyncio.gather(
                receive_from_client(),
                receive_from_gemini()
            )
            
    except Exception as e:
        print(f"Error in Gemini Session: {e}")
        await websocket.close()

async def main():
    print("Starting Bidirectional Voice Translator on ws://0.0.0.0:8091")
    async with websockets.serve(gemini_session_handler, "0.0.0.0", 8091):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())
