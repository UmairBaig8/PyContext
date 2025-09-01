from dataclasses import dataclass
from typing import Dict, Any, Optional
from enum import Enum
import uuid

class WorkflowState(Enum):
    PENDING = "pending"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"

class Priority(Enum):
    HIGH = 1
    MEDIUM = 2
    LOW = 3

@dataclass
class WorkflowContext:
    id: str
    data: Dict[str, Any]
    request: Optional[Dict[str, Any]] = None
    logger: Optional[Any] = None
    
    @classmethod
    def create(cls, **kwargs):
        return cls(id=str(uuid.uuid4()), data={}, **kwargs)

@dataclass
class WorkflowCheckpoint:
    workflow_id: str
    current_step: int
    state: WorkflowState
    context_data: Dict[str, Any]
    metadata: Dict[str, Any]

@dataclass
class WorkflowMessage:
    priority: Priority
    workflow_name: str
    context: WorkflowContext
    
    def __lt__(self, other):
        return self.priority.value < other.priority.value