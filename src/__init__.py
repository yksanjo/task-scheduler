"""Task Scheduler - Advanced task scheduling for multi-agent systems."""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
import uuid
import heapq


class TaskStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class AgentType(Enum):
    NVIDIA_GPU = "nvidia"
    AWS_TRAINIUM = "trainium"
    GOOGLE_TPU = "tpu"
    CPU = "cpu"


class Protocol(Enum):
    MCP = "mcp"
    A2A = "a2a"
    CUSTOM = "custom"
    HTTP = "http"


@dataclass
class ScheduledTask:
    task_id: str
    description: str
    priority: int = 0
    scheduled_time: Optional[datetime] = None
    status: TaskStatus = TaskStatus.PENDING
    retry_count: int = 0
    max_retries: int = 3
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __lt__(self, other):
        if self.scheduled_time and other.scheduled_time:
            return self.scheduled_time < other.scheduled_time
        return self.priority > other.priority


class TaskScheduler:
    """Advanced task scheduler with priority and time-based scheduling."""
    
    def __init__(self, max_retries: int = 3):
        self.tasks: Dict[str, ScheduledTask] = {}
        self.queue: List[ScheduledTask] = []
        self.max_retries = max_retries
    
    def schedule(self, task_id: str, description: str, priority: int = 0, scheduled_time: Optional[datetime] = None, max_retries: int = None) -> ScheduledTask:
        task = ScheduledTask(
            task_id=task_id,
            description=description,
            priority=priority,
            scheduled_time=scheduled_time,
            max_retries=max_retries or self.max_retries
        )
        self.tasks[task_id] = task
        heapq.heappush(self.queue, task)
        return task
    
    def unschedule(self, task_id: str) -> bool:
        task = self.tasks.get(task_id)
        if task:
            task.status = TaskStatus.CANCELLED
            return True
        return False
    
    def get_next(self) -> Optional[ScheduledTask]:
        while self.queue:
            task = heapq.heappop(self.queue)
            if task.status == TaskStatus.PENDING:
                return task
        return None
    
    def complete(self, task_id: str, success: bool = True) -> bool:
        task = self.tasks.get(task_id)
        if not task:
            return False
        
        task.status = TaskStatus.COMPLETED if success else TaskStatus.FAILED
        
        if not success and task.retry_count < task.max_retries:
            task.retry_count += 1
            task.status = TaskStatus.PENDING
            heapq.heappush(self.queue, task)
        
        return True
    
    def get_pending(self) -> List[ScheduledTask]:
        return [t for t in self.tasks.values() if t.status == TaskStatus.PENDING]
    
    def get_statistics(self) -> Dict[str, Any]:
        return {
            "total_tasks": len(self.tasks),
            "pending": len(self.get_pending()),
            "completed": len([t for t in self.tasks.values() if t.status == TaskStatus.COMPLETED]),
            "failed": len([t for t in self.tasks.values() if t.status == TaskStatus.FAILED])
        }


__all__ = ["TaskScheduler", "ScheduledTask", "TaskStatus", "AgentType", "Protocol"]
