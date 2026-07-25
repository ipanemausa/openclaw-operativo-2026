# claw-orchestrator/app/queue_manager.py
import math

class QueueManager:
    """
    Queueing Theory M/M/c model for orchestrator.
    Evaluates the system state based on arrival rate (lambda),
    service rate (mu), and number of workers (c).
    """
    def __init__(self, num_workers=1):
        self.c = num_workers
        # Historical trackers for lambda (arrivals per sec) and mu (services per sec)
        self.lambda_rate = 0.01  # safe default
        self.mu_rate = 0.1       # safe default
        
    def update_metrics(self, lambda_rate, mu_rate, num_workers=None):
        self.lambda_rate = max(0.0001, lambda_rate)
        self.mu_rate = max(0.0001, mu_rate)
        if num_workers is not None:
            self.c = max(1, num_workers)
            
    def calculate_rho(self):
        """Traffic intensity / utilization (rho = lambda / c*mu)"""
        return self.lambda_rate / (self.c * self.mu_rate)
        
    def calculate_p0(self, rho):
        """Probability of zero tasks in the system"""
        if rho >= 1: return 0.0 # unstable
        
        sum_prob = 0
        for n in range(self.c):
            sum_prob += ((self.c * rho) ** n) / math.factorial(n)
            
        term2 = ((self.c * rho) ** self.c) / (math.factorial(self.c) * (1 - rho))
        return 1.0 / (sum_prob + term2)
        
    def calculate_Lq(self, rho, p0):
        """Average number of tasks waiting in queue"""
        if rho >= 1: return float('inf')
        numerator = p0 * ((self.lambda_rate / self.mu_rate) ** self.c) * rho
        denominator = math.factorial(self.c) * ((1 - rho) ** 2)
        return numerator / denominator
        
    def get_queue_metrics(self):
        """Returns all M/M/c metrics"""
        rho = self.calculate_rho()
        
        # If system is unstable, return infinite waits
        if rho >= 1:
            return {
                "rho": rho,
                "Lq": float('inf'), # waiting in queue
                "L": float('inf'),  # total in system
                "Wq": float('inf'), # wait time in queue
                "W": float('inf'),  # total time in system
                "is_stable": False
            }
            
        p0 = self.calculate_p0(rho)
        Lq = self.calculate_Lq(rho, p0)
        L = Lq + (self.lambda_rate / self.mu_rate)
        Wq = Lq / self.lambda_rate
        W = Wq + (1 / self.mu_rate)
        
        return {
            "rho": rho,
            "Lq": Lq,
            "L": L,
            "Wq": Wq,
            "W": W,
            "is_stable": True
        }
