/**
 * ==============================================================================
 * OPENCLAW 2026 / HB.OS — OMNIROUTER & VECTORIAL EMBEDDINGS DAG R768
 * ==============================================================================
 * Endpoint Serverless para Vercel: POST /api/update-embeddings
 * 
 * OBJETIVO:
 * Reemplazar vectores SHA-256 por embeddings semánticos reales usando la API
 * de Hugging Face (sentence-transformers/all-MiniLM-L6-v2).
 * 
 * FASES DEL DAG:
 * 1. Endpoint POST /api/update-embeddings (sin credenciales requeridas en body)
 * 2. Extracción de puntos de la colección 'registro_ecosistema' desde Qdrant
 * 3. Inferencia de embeddings reales vía Hugging Face API con fallback SHA-256
 * 4. Upsert de puntos con vectores actualizados preservando payload original
 * 5. Verificación semántica Top-5 con query "proveedor deepseek"
 * 6. Reporte de puntos actualizados sin exponer secretos
 * ==============================================================================
 */

import crypto from 'crypto';

// Configuración de constantes y endpoints
const HF_MODEL_ENDPOINT = "https://api-inference.huggingface.co/pipeline/feature-extraction/sentence-transformers/all-MiniLM-L6-v2";
const HF_FALLBACK_ENDPOINT = "https://router.huggingface.co/hf-inference/models/sentence-transformers/all-MiniLM-L6-v2";
const COLLECTION_NAME = "registro_ecosistema";

/**
 * Genera un vector SHA-256 determinista de fallback si la API falla
 * @param {string} text 
 * @param {number} dimensions 
 * @returns {number[]}
 */
function generateSha256Vector(text, dimensions = 384) {
    const hash = crypto.createHash('sha256').update(text || '').digest('hex');
    const vector = [];
    for (let i = 0; i < dimensions; i++) {
        const sub = hash.slice((i * 2) % (hash.length - 2), (i * 2) % (hash.length - 2) + 2);
        const val = (parseInt(sub || '00', 16) / 255.0) * 2.0 - 1.0;
        vector.push(parseFloat(val.toFixed(6)));
    }
    return vector;
}

/**
 * Obtiene el embedding de un texto vía Hugging Face Inference API
 * @param {string} text 
 * @param {string} [hfApiKey]
 * @returns {Promise<number[] | null>}
 */
async function fetchHuggingFaceEmbedding(text, hfApiKey) {
    const headers = {
        'Content-Type': 'application/json'
    };
    if (hfApiKey) {
        headers['Authorization'] = `Bearer ${hfApiKey}`;
    }

    const payload = JSON.stringify({
        inputs: text,
        options: { wait_for_model: true }
    });

    const endpoints = [HF_MODEL_ENDPOINT, HF_FALLBACK_ENDPOINT];

    for (const endpoint of endpoints) {
        try {
            const controller = new AbortController();
            const timeoutId = setTimeout(() => controller.abort(), 12000);

            const response = await fetch(endpoint, {
                method: 'POST',
                headers,
                body: payload,
                signal: controller.signal
            });
            clearTimeout(timeoutId);

            if (response.ok) {
                const data = await response.json();
                if (Array.isArray(data)) {
                    // Si viene anidado [[...]], aplanar
                    return Array.isArray(data[0]) ? data[0] : data;
                }
            }
        } catch (err) {
            console.warn(`[HF-EMBEDDINGS] Fallo en endpoint ${endpoint}:`, err.message);
        }
    }
    return null;
}

/**
 * Recupera todos los puntos de la colección en Qdrant usando Scroll API
 * @param {string} qdrantUrl 
 * @param {string} qdrantApiKey 
 * @param {string} collection 
 * @returns {Promise<Array<object>>}
 */
async function fetchAllQdrantPoints(qdrantUrl, qdrantApiKey, collection) {
    const points = [];
    let nextPageOffset = null;
    const cleanUrl = qdrantUrl.replace(/\/+$/, '');

    const headers = {
        'Content-Type': 'application/json'
    };
    if (qdrantApiKey) {
        headers['api-key'] = qdrantApiKey;
    }

    do {
        const body = {
            limit: 100,
            with_payload: true,
            with_vector: true
        };
        if (nextPageOffset) {
            body.offset = nextPageOffset;
        }

        const res = await fetch(`${cleanUrl}/collections/${collection}/points/scroll`, {
            method: 'POST',
            headers,
            body: JSON.stringify(body)
        });

        if (!res.ok) {
            const errText = await res.text();
            throw new Error(`Error en Qdrant scroll (${res.status}): ${errText}`);
        }

        const data = await res.json();
        const batch = data.result?.points || [];
        points.push(...batch);

        nextPageOffset = data.result?.next_page_offset;
    } while (nextPageOffset);

    return points;
}

/**
 * Ejecuta el DAG completo de actualización de embeddings
 */
export async function executeUpdateEmbeddingsDAG() {
    const qdrantUrl = process.env.QDRANT_URL || process.env.QDRANT_HOST;
    const qdrantApiKey = process.env.QDRANT_API_KEY;
    const hfApiKey = process.env.HUGGINGFACE_API_KEY || process.env.HF_TOKEN || process.env.HUGGING_FACE_HUB_TOKEN;

    if (!qdrantUrl) {
        throw new Error("Variable de entorno QDRANT_URL no configurada.");
    }

    const cleanQdrantUrl = qdrantUrl.replace(/\/+$/, '');
    const qdrantHeaders = {
        'Content-Type': 'application/json'
    };
    if (qdrantApiKey) {
        qdrantHeaders['api-key'] = qdrantApiKey;
    }

    // FASE 2: Obtener puntos existentes
    console.log(`[DAG-R768] FASE 2: Leyendo puntos de colección '${COLLECTION_NAME}'...`);
    const points = await fetchAllQdrantPoints(cleanQdrantUrl, qdrantApiKey, COLLECTION_NAME);
    console.log(`[DAG-R768] Puntos recuperados: ${points.length}`);

    if (points.length === 0) {
        return {
            status: "success",
            message: "No se encontraron puntos existentes en la colección para actualizar.",
            points_updated: 0,
            verification_top5: []
        };
    }

    // FASE 3 & FASE 4: Generar embeddings reales y preparar puntos para Upsert
    console.log(`[DAG-R768] FASE 3: Generando embeddings semánticos reales vía Hugging Face...`);
    const updatedPoints = [];
    let hfSuccessCount = 0;
    let fallbackCount = 0;

    for (const pt of points) {
        const payload = pt.payload || {};
        const nombre = payload.nombre || payload.name || payload.title || '';
        const tipo = payload.tipo || payload.type || payload.categoria || '';
        const descripcion = payload.descripcion || payload.description || payload.content || '';

        const textToEmbed = `${nombre} ${tipo} ${descripcion}`.trim() || JSON.stringify(payload);

        let realVector = await fetchHuggingFaceEmbedding(textToEmbed, hfApiKey);

        if (realVector && realVector.length > 0) {
            hfSuccessCount++;
        } else {
            fallbackCount++;
            // Conservar vector existente si existe, o usar vector determinista SHA-256
            realVector = pt.vector && Array.isArray(pt.vector) && pt.vector.length > 0
                ? pt.vector
                : generateSha256Vector(textToEmbed, 384);
        }

        updatedPoints.push({
            id: pt.id,
            vector: realVector,
            payload: pt.payload
        });
    }

    // FASE 4: Upsert con nuevos vectores en lotes de 50
    console.log(`[DAG-R768] FASE 4: Ejecutando Upsert en Qdrant (${updatedPoints.length} puntos)...`);
    const BATCH_SIZE = 50;
    for (let i = 0; i < updatedPoints.length; i += BATCH_SIZE) {
        const batch = updatedPoints.slice(i, i + BATCH_SIZE);
        const upsertRes = await fetch(`${cleanQdrantUrl}/collections/${COLLECTION_NAME}/points`, {
            method: 'PUT',
            headers: qdrantHeaders,
            body: JSON.stringify({ points: batch })
        });

        if (!upsertRes.ok) {
            const err = await upsertRes.text();
            throw new Error(`Error en Qdrant upsert batch ${i}-${i + batch.length}: ${err}`);
        }
    }

    // FASE 5: Verificación Semántica ("proveedor deepseek")
    console.log(`[DAG-R768] FASE 5: Verificando consulta de prueba 'proveedor deepseek'...`);
    const testQuery = "proveedor deepseek";
    let queryVector = await fetchHuggingFaceEmbedding(testQuery, hfApiKey);
    if (!queryVector) {
        queryVector = generateSha256Vector(testQuery, 384);
    }

    const searchRes = await fetch(`${cleanQdrantUrl}/collections/${COLLECTION_NAME}/points/search`, {
        method: 'POST',
        headers: qdrantHeaders,
        body: JSON.stringify({
            vector: queryVector,
            limit: 5,
            with_payload: true
        })
    });

    let top5 = [];
    if (searchRes.ok) {
        const searchData = await searchRes.json();
        top5 = (searchData.result || []).map(hit => ({
            id: hit.id,
            score: hit.score,
            payload: hit.payload
        }));
    } else {
        console.warn("[DAG-R768] Aviso al consultar Top-5 de verificación:", await searchRes.text());
    }

    // FASE 6: Cierre y reporte sanitizado
    return {
        status: "success",
        dag: "DAG-R768-EMBEDDINGS-UPDATE",
        timestamp: new Date().toISOString(),
        points_total: points.length,
        points_updated: updatedPoints.length,
        hf_embeddings_generated: hfSuccessCount,
        fallbacks_used: fallbackCount,
        query_verification: testQuery,
        verification_top_5: top5
    };
}

/**
 * Handler Vercel Serverless Function
 * Ruta: POST /api/update-embeddings
 */
export default async function handler(req, res) {
    // Permitir CORS
    res.setHeader('Access-Control-Allow-Credentials', true);
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET,OPTIONS,PATCH,DELETE,POST,PUT');
    res.setHeader(
        'Access-Control-Allow-Headers',
        'X-CSRF-Token, X-Requested-With, Accept, Accept-Version, Content-Length, Content-MD5, Content-Type, Date, X-Api-Version'
    );

    if (req.method === 'OPTIONS') {
        return res.status(200).end();
    }

    if (req.method !== 'POST') {
        return res.status(405).json({
            error: "Method Not Allowed. Envíe una solicitud POST a /api/update-embeddings"
        });
    }

    try {
        const result = await executeUpdateEmbeddingsDAG();
        return res.status(200).json(result);
    } catch (error) {
        console.error("[DAG-R768] Error durante ejecución:", error.message);
        return res.status(500).json({
            status: "error",
            error: error.message,
            timestamp: new Date().toISOString()
        });
    }
}
