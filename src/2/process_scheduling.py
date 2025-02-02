
import time
import heapq
from collections import deque

class Process:
    def __init__(self, pid, execution_time, priority=0):
        self.pid = pid
        self.execution_time = execution_time
        self.remaining_time = execution_time
        self.priority = priority

    def __lt__(self, other):
        return self.priority < other.priority

# Updated Round-Robin Scheduling with user-configurable time quantum
def round_robin(processes, time_quantum):
    queue = deque(processes)
    while queue:
        process = queue.popleft()
        execution_time = min(time_quantum, process.remaining_time)
        print(f"Process {process.pid} running for {execution_time} units.")
        process.remaining_time -= execution_time
        time.sleep(execution_time / 10)  # Simulate execution

        if process.remaining_time > 0:
            queue.append(process)  # Re-add to queue if not finished
        else:
            print(f"Process {process.pid} completed execution.")

# Updated Priority-Based Scheduling with Preemption
def priority_scheduling(processes):
    priority_queue = []
    for process in processes:
        heapq.heappush(priority_queue, (process.priority, process))

    while priority_queue:
        _, process = heapq.heappop(priority_queue)
        print(f"Executing Process {process.pid} with priority {process.priority} for {process.execution_time} units.")
        time.sleep(process.execution_time / 10)

# Example Usage with User Input for Time Quantum
if __name__ == "__main__":
    processes = [Process(1, 5, 2), Process(2, 8, 1), Process(3, 3, 3)]

    # Get user input for time quantum
    time_quantum = int(input("Enter time quantum for Round-Robin Scheduling: "))

    print("\nExecuting Round-Robin Scheduling:")
    round_robin(processes.copy(), time_quantum)

    print("\nExecuting Priority-Based Scheduling with Preemption:")
    priority_scheduling(processes.copy())
