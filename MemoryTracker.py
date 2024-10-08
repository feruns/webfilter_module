import time
import psutil
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

class MemoryMonitor:
    def __init__(self, process_names):
        self.process_names = process_names
        self.memory_usage = {}  # Dictionary to hold memory usage per process
        self.timestamps = []
        self.processes = []

    def _get_processes(self):
        self.processes = [p for p in psutil.process_iter(['pid', 'name']) if p.info['name'] in self.process_names]
        # Initialize the memory usage dictionary with process names
        for process in self.processes:
            self.memory_usage[process.info['name']] = []

    def start_monitoring(self, interval=10):
        self._get_processes()
        while True:
            current_time = time.time()
            self.timestamps.append(current_time)
            for process in self.processes:
                if process.is_running():
                    usage = process.memory_info().rss / (1024 * 1024)  # Memory usage in MB
                    self.memory_usage[process.info['name']].append(usage)
                else:
                    self.memory_usage[process.info['name']].append(0)  # In case the process is not running
            time.sleep(interval)

    def stop_monitoring(self):
        self.monitoring = False

    def check_memory_growth(self, significance_level=0.05):
        results = {}
        for process_name, usage_list in self.memory_usage.items():
            if len(usage_list) < 2:
                results[process_name] = (False, "Insufficient data for analysis")
                continue
            
            # Perform a linear regression for each process to see if there is memory growth over time
            slope, intercept, r_value, p_value, std_err = stats.linregress(self.timestamps, usage_list)
            if p_value < significance_level and slope > 0:
                results[process_name] = (True, f"Memory growth detected for {process_name} with p-value {p_value:.5f} and slope {slope:.5f}")
            else:
                results[process_name] = (False, f"No significant memory growth detected for {process_name}")
        
        return results

    def save_memory_plot(self, output_file="memory_usage.png"):
        plt.figure(figsize=(10, 6))
        for process_name, usage_list in self.memory_usage.items():
            plt.plot(self.timestamps, usage_list, label=f"Memory Usage for {process_name} (MB)")
        
        plt.xlabel("Time (s)")
        plt.ylabel("Memory (MB)")
        plt.title("Memory Usage Over Time")
        plt.legend()
        plt.savefig(output_file)

# Example methods callable from Robot Framework
monitor = None

def start_memory_monitoring(process_names, interval=10):
    global monitor
    monitor = MemoryMonitor(process_names)
    monitor.start_monitoring(interval)

def stop_memory_monitoring_and_check_growth():
    global monitor
    if monitor is not None:
        results = monitor.check_memory_growth()
        monitor.save_memory_plot()
        for process_name, (growth_detected, message) in results.items():
            print(f"{process_name}: {message}")
            if growth_detected:
                return True, message  # If any process has memory growth, return failure
        return False, "No memory growth detected for any process"
    return False, "No monitor instance available"
