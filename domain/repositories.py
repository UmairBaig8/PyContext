from abc import ABC, abstractmethod
from typing import Optional
from .entities import WorkflowCheckpoint

class CheckpointRepository(ABC):
    @abstractmethod
    async def save(self, checkpoint: WorkflowCheckpoint) -> None:
        pass
    
    @abstractmethod
    async def load(self, workflow_id: str) -> Optional[WorkflowCheckpoint]:
        pass
    
    @abstractmethod
    async def delete(self, workflow_id: str) -> None:
        pass