import os
import json
import urllib.request
import urllib.error
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="OpenClaw Financial RAG Worker")

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")

@app.get("/health")
def health():
    engines = []
    if DEEPSEEK_API_KEY:
        engines.append("deepseek")
    if OPENROUTER_API_KEY:
        engines.append("openrouter_qwen")
    if GEMINI_API_KEY:
        engines.append("gemini")
    return {
        "service": "financial_rag_worker",
        "status": "healthy",
        "engines_ready": engines,
        "default_engine": engines[0] if engines else "none"
    }

@app.get("/")
def root():
    return {"service": "financial_rag_worker", "status": "running"}

class QueryRequest(BaseModel):
    query: str

def call_deepseek(prompt: str) -> str:
    url = "https://api.deepseek.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "Eres el asistente financiero y de negocios de HB Jewelry. Respondes con datos concretos y concisos."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 1024,
        "temperature": 0.2
    }
    req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=20) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        return data["choices"][0]["message"]["content"]

def call_openrouter(prompt: str) -> str:
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://openclaw.cloud",
        "X-Title": "OpenClaw Financial RAG"
    }
    payload = {
        "model": "qwen/qwen-2.5-72b-instruct",
        "messages": [
            {"role": "system", "content": "Eres el asistente financiero y de negocios de HB Jewelry. Respondes con datos concretos y concisos."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 1024,
        "temperature": 0.2
    }
    req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=20) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        return data["choices"][0]["message"]["content"]

@app.post("/api/rag/query")
async def rag_query(request: QueryRequest):
    prompt = (
        f"Contexto Financiero HB Jewelry & OpenClaw. "
        f"Analiza la siguiente consulta y responde de forma practica y accionable: {request.query}"
    )

    # 1. Intentar DeepSeek ($0 cost, ultra rapido)
    if DEEPSEEK_API_KEY:
        try:
            answer = call_deepseek(prompt)
            return {"answer": answer, "engine": "deepseek"}
        except Exception as e:
            print(f"[RAG WORKER] DeepSeek fallback: {e}")

    # 2. Intentar OpenRouter Qwen ($0 cost free tier)
    if OPENROUTER_API_KEY:
        try:
            answer = call_openrouter(prompt)
            return {"answer": answer, "engine": "qwen"}
        except Exception as e:
            print(f"[RAG WORKER] OpenRouter fallback: {e}")

    # 3. Fallback a Gemini Flash 2.0 via Google API
    if GEMINI_API_KEY:
        try:
            from google import genai
            client = genai.Client(api_key=GEMINI_API_KEY)
            response = client.models.generate_content(
                model='gemini-2.0-flash',
                contents=prompt,
            )
            return {"answer": response.text, "engine": "gemini-2.0-flash"}
        except Exception as e:
            return {"error": f"Error en fallback Gemini: {str(e)}"}

    return {"error": "No hay API keys configuradas en el RAG worker."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8093)
