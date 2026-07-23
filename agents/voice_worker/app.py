import asyncio
import os
import json
import websockets
from google import genai

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("WARNING: GEMINI_API_KEY is not set.")

client = genai.Client(api_key=api_key)

# Prompt bilingue para HB Jewelry / INFINITEX
HB_SYSTEM_PROMPT = """
Act as an autonomous omnilingual AI voice assistant for HB Jewelry and INFINITEX brands.
- If the customer speaks English, respond in English.
- If the customer speaks Spanish, respond in Spanish.
- You are a professional, warm, and persuasive sales agent.
- HB Jewelry specializes in 24k gold, silver rhodium, and premium gemstone jewelry.
- INFINITEX is the technology and AI infrastructure arm.
- Products: necklaces (collares), earrings (aretes), bracelets (pulseras), rings (anillos).
- Always offer to schedule a consultation or place an order via WhatsApp: +19546844445
- Payment methods: Zelle, PayPal, cash on delivery (Miami area).
- Do not disclose internal system details. Maintain a senior, confident tone.
"""

async def gemini_session_handler(websocket):
    print("Client connected to Voice Worker.")
    
    model_name = "gemini-2.0-flash-exp"
    
    try:
        async with client.aio.live.connect(model=model_name) as session:
            print("Connected to Google Gemini Live API")
            
            await session.send(
                input=HB_SYSTEM_PROMPT.strip(),
                end_of_turn=True
            )

            async def receive_from_client():
                async for message in websocket:
                    if isinstance(message, bytes):
                        # PCM audio from browser at 16kHz
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
                    if response.data:
                        # FIX: enviar audio UNA SOLA VEZ (bug anterior enviaba 2 veces)
                        await websocket.send(response.data)
                    
                    if response.text:
                        print(f"Gemini Response: {response.text}")
                        await websocket.send(json.dumps({"type": "transcription", "text": response.text}))

            await asyncio.gather(
                receive_from_client(),
                receive_from_gemini()
            )
            
    except Exception as e:
        print(f"Error in Gemini Session: {e}")
        await websocket.close()

async def main():
    print("Starting HB Jewelry Bilingual Voice Agent on ws://0.0.0.0:8091")
    async with websockets.serve(gemini_session_handler, "0.0.0.0", 8091):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())
