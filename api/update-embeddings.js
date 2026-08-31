/**
 * Vercel Serverless Function: POST /api/update-embeddings
 * Exporta el handler desde omnirouter_hbos.js
 */
import handler, { executeUpdateEmbeddingsDAG } from '../omnirouter_hbos.js';

export { executeUpdateEmbeddingsDAG };
export default handler;
