import express from 'express';
import { setupWorker } from './queue/TaskWorker.js';

const app = express();
app.use(express.json());

app.post('/api/webhook/n8n/trigger', (req, res) => {
    console.log('[ORCHESTRATOR] Webhook received from N8N:', req.body);
    // En un flujo real, esto se empuja a BullMQ
    res.json({ status: 'queued', message: 'N8N payload received' });
});

const PORT = process.env.PORT || 8090;

app.listen(PORT, () => {
    console.log(`[ORCHESTRATOR] Node.js Server listening on port ${PORT}`);
    setupWorker();
});
