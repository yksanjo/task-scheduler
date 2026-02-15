# Task Scheduler

Advanced task scheduling for multi-agent systems.

## Features

- **Priority Scheduling** - Priority-based task ordering
- **Time-based Scheduling** - Schedule tasks for specific times
- **Batch Processing** - Process multiple tasks together
- **Retry Logic** - Automatic retry on failure

## Quick Start

```python
from task_scheduler import TaskScheduler

scheduler = TaskScheduler()
scheduler.schedule("task-1", priority=1)
next_task = scheduler.get_next()
```

## License

MIT
