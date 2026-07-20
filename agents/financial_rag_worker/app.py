import os
from fastapi import FastAPI
from pydantic import BaseModel
from google import genai
from google.genai import types

# Configuracion basica del servidor FastAPI para el motor RAG Matemático
app = FastAPI()

api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key) if api_key else None

class QueryRequest(BaseModel):
    query: str

@app.post("/api/rag/query")
async def rag_query(request: QueryRequest):
    if not client:
        return {"error": "GEMINI_API_KEY no está configurado."}
    
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
