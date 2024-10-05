# lib/memory_tracker.py

import psutil
import time
import numpy as np

class ProcessMemoryTracker:
    def __init__(self, pids, window_size=5, growth_threshold=5):
        self.pids = pids
        self.memory_usage_history = {pid: [] for pid in pids}
        self.window_size = window_size
        self.growth_threshold = growth_threshold

    def get_memory_usage(self, pid):
        try:
            process = psutil.Process(pid)
            return process.memory_info().rss / 1024  # Memory in KB
        except psutil.NoSuchProcess:
            return None

    def collect_memory_usage(self):
        for pid in self.pids:
            memory = self.get_memory_usage(pid)
            if memory is not None:
                self.memory_usage_history[pid].append(memory)
                if len(self.memory_usage_history[pid]) > self.window_size:
                    self.memory_usage_history[pid].pop(0)
            else:
                print("Process with PID {} not found.".format(pid))

    def detect_memory_growth(self):
        memory_growth = {}
        for pid, usage_history in self.memory_usage_history.items():
            if len(usage_history) >= self.window_size:
                avg_before = np.mean(usage_history[:-1])
                current_usage = usage_history[-1]
                std_dev = np.std(usage_history[:-1])
                percentage_increase = ((current_usage - avg_before) / avg_before) * 100
                if percentage_increase > self.growth_threshold + std_dev:
                    memory_growth[pid] = True
                else:
                    memory_growth[pid] = False
            else:
                memory_growth[pid] = None
        return memory_growth
