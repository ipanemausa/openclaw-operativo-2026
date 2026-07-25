# claw-orchestrator/app/cpm_pipeline.py
from collections import defaultdict

def calculate_cpm(tasks):
    """
    Calculates Critical Path Method (CPM) metrics for a DAG of tasks.
    tasks: dict of { task_id: {"duration": float, "depends_on": [task_id, ...]} }
    
    Returns a dict with early start/finish, late start/finish, slack, and critical flag.
    """
    # 1. Forward Pass (Early Start & Early Finish)
    es = {}
    ef = {}
    
    # Sort topologically to process dependencies first
    # Simple algorithm since we assume a valid DAG
    processed = set()
    
    def process_forward(node):
        if node in processed: return
        t = tasks[node]
        deps = t.get("depends_on", [])
        for d in deps:
            if d not in processed:
                process_forward(d)
        
        # ES is max of EF of all dependencies
        my_es = max([ef[d] for d in deps]) if deps else 0.0
        my_ef = my_es + t.get("duration", 0.0)
        es[node] = my_es
        ef[node] = my_ef
        processed.add(node)
        
    for t_id in tasks:
        process_forward(t_id)
        
    # 2. Backward Pass (Late Start & Late Finish)
    ls = {}
    lf = {}
    
    # Project end time is the maximum of all Early Finishes
    project_duration = max(ef.values()) if ef else 0.0
    
    # Find reverse dependencies (who depends on me)
    rev_deps = defaultdict(list)
    for t_id, data in tasks.items():
        for d in data.get("depends_on", []):
            rev_deps[d].append(t_id)
            
    processed_back = set()
    
    def process_backward(node):
        if node in processed_back: return
        dependents = rev_deps[node]
        for d in dependents:
            if d not in processed_back:
                process_backward(d)
        
        # LF is min of LS of all dependents, or project duration if none
        my_lf = min([ls[d] for d in dependents]) if dependents else project_duration
        my_ls = my_lf - tasks[node].get("duration", 0.0)
        
        lf[node] = my_lf
        ls[node] = my_ls
        processed_back.add(node)
        
    for t_id in tasks:
        process_backward(t_id)
        
    # 3. Calculate Slack and identify Critical Path
    cpm_results = {}
    critical_path = []
    
    for t_id in tasks:
        slack = ls[t_id] - es[t_id]
        is_critical = abs(slack) < 1e-5
        if is_critical:
            critical_path.append(t_id)
            
        cpm_results[t_id] = {
            "es": es[t_id],
            "ef": ef[t_id],
            "ls": ls[t_id],
            "lf": lf[t_id],
            "slack": slack,
            "is_critical": is_critical
        }
        
    return {
        "project_duration": project_duration,
        "critical_path": critical_path,
        "tasks": cpm_results
    }
