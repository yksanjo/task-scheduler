#!/usr/bin/env python3
"""Demo for Task Scheduler."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src import TaskScheduler

def main():
    print("Task Scheduler Demo")
    ts = TaskScheduler()
    ts.schedule("t1", "Task 1", priority=1)
    ts.schedule("t2", "Task 2", priority=2)
    next_task = ts.get_next()
    print(f"Next: {next_task.description if next_task else 'None'}")
    print("Done!")

if __name__ == "__main__": main()
