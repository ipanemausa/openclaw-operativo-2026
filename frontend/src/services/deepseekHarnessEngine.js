/* src/services/deepseekHarnessEngine.js */

/**
 * Motor Directo DeepSeek Harness (V4/V5 Standard)
 * Conexión nativa ultra-rápida y desacoplada de MCP.
 */

const API_BASE = "";

export class DeepSeekHarnessEngine {
  /**
   * Envía una consulta directamente a la pasarela DeepSeek Harness
   * @param {string} userMessage - Mensaje del usuario
   * @param {string} agent - Identificador del agente ('bilingual_cs', 'marketing', etc.)
   * @param {string} model - Modelo de DeepSeek ('deepseek-chat' o 'deepseek-reasoner')
   */
  static async queryDeepSeek(userMessage, agent = "bilingual_cs", model = "deepseek-chat") {
    try {
      const response = await fetch(API_BASE + "/api/deepseek/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ agent, message: userMessage, model }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error ${response.status}`);
      }

      const data = await response.json();
      return {
        success: true,
        response: data.response,
        provider: data.provider || "deepseek_harness",
        model: data.model || model,
      };
    } catch (error) {
      console.warn("DeepSeek Harness offline/error, utilizando motor RAG secundario:", error);
      return {
        success: false,
        error: error.message,
      };
    }
  }
}
