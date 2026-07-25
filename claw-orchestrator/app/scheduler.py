# claw-orchestrator/app/scheduler.py
from cpm_pipeline import calculate_cpm
from queue_manager import QueueManager

class EnterpriseScheduler:
    def __init__(self):
        # Dictionary of queue managers for different worker types
        self.queues = {
            "chat": QueueManager(num_workers=2),
            "video": QueueManager(num_workers=1),
            "rag": QueueManager(num_workers=1)
        }
        
    def evaluate_task(self, task_id, task_data, dag_tasks):
        """
        Evaluate if a task should be scheduled immediately or delayed.
        task_data: dict with "type" (e.g., chat, video), "duration", "depends_on"
        dag_tasks: all tasks in the current job to calculate CPM
        """
        # 1. Calculate CPM
        cpm_results = calculate_cpm(dag_tasks)
        task_cpm = cpm_results["tasks"].get(task_id, {})
        is_critical = task_cpm.get("is_critical", False)
        
        # 2. Get Queue metrics
        task_type = task_data.get("type", "chat")
        queue = self.queues.get(task_type, self.queues["chat"])
        metrics = queue.get_queue_metrics()
        
        # 3. Decision Logic
        action = "SCHEDULE"
        reason = ""
        
        if not metrics["is_stable"] or metrics["rho"] > 0.85:
            # System is under heavy load
            if is_critical:
                action = "SCHEDULE_PRIORITY"
                reason = f"Critical path task pushed through heavy load (rho={metrics['rho']:.2f})"
            else:
                action = "DELAY"
                reason = f"Non-critical task delayed due to load (rho={metrics['rho']:.2f}, slack={task_cpm.get('slack', 0):.2f})"
        else:
            action = "SCHEDULE"
            reason = f"Normal load (rho={metrics['rho']:.2f}), normal scheduling."
            
        return {
            "action": action,
            "reason": reason,
            "metrics": metrics,
            "cpm": task_cpm
        }
