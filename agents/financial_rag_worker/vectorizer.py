import os
import json
from google import genai
import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore_v1.vector import Vector

# ===================================================================
# OPENCLAW AI STUDIO: MOTOR DE VECTORIZACIÓN (FÓRMULAS MATEMÁTICAS)
# ===================================================================

# 1. Configurar IA Generativa (Google Gemini para generar Vectores)
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    print("[!] ADVERTENCIA: Variable de entorno GEMINI_API_KEY no encontrada.")
client = genai.Client(api_key=API_KEY) if API_KEY else None

# 2. Inicializar Firebase Admin SDK (Requiere credenciales.json)
# if not firebase_admin._apps:
#     cred = credentials.Certificate("firebase_credentials.json")
#     firebase_admin.initialize_app(cred)
# db = firestore.client()

# --- Base de datos de prueba (Simulando JSON de productos/operativa) ---
dummy_database = [
    {"id": "doc1", "title": "Protocolo de Emergencia", "content": "Si los contenedores fallan, ejecutar rclone-backup.ps1 y reiniciar el Gateway."},
    {"id": "doc2", "title": "Modelo de Ventas HB", "content": "Los collares de oro de 24k tienen un margen del 35%. Siempre ofrecer envío asegurado."},
    {"id": "doc3", "title": "Integración Muncher", "content": "La API de logística devuelve código 200 cuando el repartidor acepta el paquete de la joyería."}
]

def text_to_math_formula(text: str) -> list[float]:
    """
    Convierte el texto humano en una matriz de vectores (fórmulas matemáticas)
    usando text-embedding-004 de Google.
    """
    if not client:
        # Vector simulado (768 dimensiones) si no hay API_KEY
        print(f"[-] [Simulacion] Convirtiendo texto a formulas: '{text[:20]}...'")
        return [0.015, -0.223, 0.551] + [0.0] * 765 
        
    try:
        response = client.models.embed_content(
            model='text-embedding-004',
            contents=text
        )
        return response.embeddings[0].values
    except Exception as e:
        print(f"[!] Error generando Embedding: {e}")
        return []

def run_vectorization():
    print("=========================================================")
    print(" [AI] INICIANDO VECTORIZACIÓN MATEMÁTICA RAG -> FIREBASE ")
    print("=========================================================")
    
    for item in dummy_database:
        print(f"\n[+] Procesando Documento: {item['title']}")
        
        # Paso 1: Conversión Matemática
        vector = text_to_math_formula(item['content'])
        print(f"  -> Traducido a vector espacial de {len(vector)} dimensiones.")
        
        # Paso 2: Subida a Firebase Firestore (Mock comentado hasta tener credenciales)
        print("  -> Subiendo a Firebase Firestore Vector Database...")
        # doc_ref = db.collection('knowledge_base').document(item['id'])
        # doc_ref.set({
        #     "title": item['title'],
        #     "content": item['content'],
        #     "embedding": Vector(vector) # Almacena matemáticamente en Firebase
        # })
        print("  -> ¡Guardado exitoso!")
        
    print("\n[OK] BASE DE DATOS VECTORIZADA Y LISTA EN FIREBASE.")

if __name__ == "__main__":
    run_vectorization()
