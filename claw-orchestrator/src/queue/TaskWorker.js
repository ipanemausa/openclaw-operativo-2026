import { routeTask } from '../routers/OmniRouter.js';
import Redis from 'ioredis';

const redis = new Redis({
    host: process.env.REDIS_HOST || 'redis',
    port: parseInt(process.env.REDIS_PORT || '6379')
});

const ECC_STATE_KEY = "ecc:state";
const ECC_AUDIT_STREAM = "ecc:audit";
const ECC_VERSION_KEY = "ecc:version";

async function eccGate(action, taskName, actor = "node_executor", success = true) {
    try {
        const ts = new Date().toISOString();
        let version = await redis.hget(ECC_STATE_KEY, "version") || "0";
        let newV = parseInt(version) + 1;

        if (action === "in") {
            await redis.hset(ECC_STATE_KEY, {
                "active_task": taskName,
                "active_task_locked_by": actor,
                "last_actor": actor,
                "last_action": `executor_gate_in:${taskName}`,
                "version": newV.toString(),
                "timestamp": ts
            });
            await redis.set(ECC_VERSION_KEY, newV.toString());
            await redis.xadd(ECC_AUDIT_STREAM, "*", 
                "version", newV.toString(), 
                "actor", actor,
                "action", "executor_gate_in", 
                "task", taskName,
                "result", "started", 
                "timestamp", ts
            );
        } else if (action === "out") {
            await redis.hset(ECC_STATE_KEY, {
                "active_task": "",
                "active_task_locked_by": "",
                "last_actor": actor,
                "last_action": `executor_gate_out:${taskName}`,
                "last_action_validated": success ? "true" : "false",
                "version": newV.toString(),
                "timestamp": ts
            });
            await redis.set(ECC_VERSION_KEY, newV.toString());
            await redis.xadd(ECC_AUDIT_STREAM, "*", 
                "version", newV.toString(), 
                "actor", actor,
                "action", "executor_gate_out", 
                "task", taskName,
                "result", success ? "success" : "failed", 
                "timestamp", ts
            );
        }
        console.log(`[ECC] gate_${action}: ${taskName}`);
    } catch (error) {
        console.error(`[ECC] gate_${action} error (non-blocking):`, error);
    }
}

export function setupWorker() {
    console.log('[WORKER] Iniciando integración nativa de cola y Trazabilidad ECC...');
    
    // Simulate consuming an event with Traceability
    setTimeout(async () => {
        const dummyTask = { name: "sandbox_task", data: "Test payload from N8N" };
        console.log(`[WORKER] Tarea recibida: ${dummyTask.name}`);
        
        await eccGate('in', dummyTask.name);
        try {
            const result = await routeTask(dummyTask);
            console.log(`[WORKER] Tarea completada exitosamente:`, result);
            await eccGate('out', dummyTask.name, "node_executor", true);
        } catch (error) {
            console.error(`[WORKER] Fallo al procesar tarea:`, error);
            await eccGate('out', dummyTask.name, "node_executor", false);
        }
    }, 2000);
}
