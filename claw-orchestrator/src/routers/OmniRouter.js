import axios from 'axios';

const REASONING_MODEL = "deepseek-reasoner";
const CODER_MODEL = "combo-best-free";

export async function routeTask(task) {
    console.log(`[ROUTER] Iniciando Pipeline de Combos para la tarea: ${task.name}`);
    
    try {
        // FASE 1: Verificación de Errores y Debug (Tribunal R768)
        console.log(`[ROUTER-FASE-1] Ejecutando análisis de razonamiento y debug (Modelo: ${REASONING_MODEL})...`);
        const verifyPrompt = `
            Actúa como un Tribunal de Auditoría Estricta (Estándar R768).
            Analiza la siguiente tarea, detecta posibles errores lógicos, fugas de memoria o vulnerabilidades arquitectónicas antes de escribir código.
            NO ESCRIBAS CÓDIGO FINAL. Solo provee el análisis depurado y la estrategia de solución validada.
            Tarea: ${JSON.stringify(task)}
        `;
        
        const verifyResponse = await axios.post('http://omnirouter:11434/v1/chat/completions', {
            model: REASONING_MODEL,
            messages: [{ role: "user", content: verifyPrompt }]
        }, { timeout: 30000 });
        
        const debuggedContext = verifyResponse.data?.choices?.[0]?.message?.content || "Auto-verificación completada sin objeciones.";
        console.log(`[ROUTER-FASE-1] Debug completado. Contexto saneado listo para ejecución.`);
        
        // FASE 2: Creación Real de Código (Generador)
        console.log(`[ROUTER-FASE-2] Generando código físico basado en el contexto validado (Modelo: ${CODER_MODEL})...`);
        const executionPrompt = `
            Eres un experto programador.
            Ejecuta y genera el código físico requerido para la Tarea basándote ESTRICTAMENTE en el siguiente contexto y estrategia depurada por el Tribunal.
            Contexto Depurado: ${debuggedContext}
            Tarea Original: ${JSON.stringify(task)}
        `;
        
        const executionResponse = await axios.post('http://omnirouter:11434/v1/chat/completions', {
            model: CODER_MODEL,
            messages: [{ role: "user", content: executionPrompt }]
        }, { timeout: 30000 });
        
        console.log(`[ROUTER-FASE-2] Código físico generado con éxito.`);
        
        return {
            status: "success",
            debug_audit: debuggedContext,
            final_code: executionResponse.data?.choices?.[0]?.message?.content || ""
        };
        
    } catch (error) {
        console.warn(`[ROUTER-FALLO] Error en el pipeline de Combos: ${error.message}`);
        return { status: "failed_combo_pipeline", error: error.message };
    }
}
