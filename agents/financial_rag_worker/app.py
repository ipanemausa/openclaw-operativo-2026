import os
from fastapi import FastAPI
from pydantic import BaseModel
from google import genai
from google.genai import types

# Configuracion basica del servidor FastAPI para el motor RAG Matemático
app = FastAPI()

api_key = os.getenv("GEMINI_API_KEY")
try:
    client = genai.Client(api_key=api_key) if api_key else None
except Exception as e:
    client = None
    print(f"[WARN] No se pudo inicializar Google GenAI Client: {e}")

@app.get("/health")
def health():
    return {"service": "financial_rag_worker", "status": "healthy", "genai_ready": client is not None}

@app.get("/")
def root():
    return {"service": "financial_rag_worker", "status": "running"}

class QueryRequest(BaseModel):
    query: str

@app.post("/api/rag/query")
async def rag_query(request: QueryRequest):
    if not client:
        return {"error": "GEMINI_API_KEY no está configurado o cliente no disponible."}
    
    # 1. (Opcional) Embeddings Matemáticos
    # Aquí es donde el texto se convertiría en vectores para buscar en tu dataset de Muncher/Teso.
    # response = client.models.embed_content(
    #     model='text-embedding-004',
    #     contents=request.query
    # )
    
    # 2. Generación con Contexto (RAG Simulado por ahora hasta tener los CSVs/JSONs)
    prompt = f"Contexto Financiero: El usuario tiene experiencia construyendo módulos financieros para Muncher y Teso. Usa RAG y Copilot logic. Pregunta: {request.query}"
    
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        return {"answer": response.text}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    # Corre en el puerto 8093 para no chocar con el Voice Worker o Avatar Hub
    uvicorn.run(app, host="0.0.0.0", port=8093)
