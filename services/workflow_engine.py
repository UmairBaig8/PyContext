import asyncio
from typing import List, Callable, Optional
from domain.entities import WorkflowContext, WorkflowCheckpoint, WorkflowState
from domain.repositories import CheckpointRepository

class WorkflowEngine:
    def __init__(self, checkpoint_repo: Optional[CheckpointRepository] = None):
        self.checkpoint_repo = checkpoint_repo
        self.steps: List[Callable] = []
        self.name = ""
    
    def configure(self, name: str, steps: List[Callable]):
        self.name = name
        self.steps = steps
    
    async def execute(self, context: WorkflowContext, start_step: int = 0) -> WorkflowContext:
        workflow_id = context.id
        
        # Load checkpoint if resuming
        if self.checkpoint_repo and start_step == 0:
            checkpoint = await self.checkpoint_repo.load(workflow_id)
            if checkpoint and checkpoint.state == WorkflowState.PAUSED:
                start_step = checkpoint.current_step
                context.data.update(checkpoint.context_data.get('data', {}))
                if context.logger:
                    context.logger.info(f"[{self.name}] Resuming from step {start_step}")
        
        # Execute steps with checkpoints
        for i in range(start_step, len(self.steps)):
            step = self.steps[i]
            
            # Save checkpoint before step
            if self.checkpoint_repo:
                checkpoint = WorkflowCheckpoint(
                    workflow_id=workflow_id,
                    current_step=i,
                    state=WorkflowState.RUNNING,
                    context_data={'data': context.data, 'request': context.request},
                    metadata={'step_name': step.__name__}
                )
                await self.checkpoint_repo.save(checkpoint)
            
            try:
                # Execute step with realistic delay
                if context.logger:
                    context.logger.info(f"[{self.name}] Starting step {i}: {step.__name__}")
                
                context = await self._execute_step(step, context)
                
                if context.logger:
                    context.logger.info(f"[{self.name}] Completed step {i}: {step.__name__}")
                    
            except asyncio.CancelledError:
                # Save pause checkpoint
                if self.checkpoint_repo:
                    pause_checkpoint = WorkflowCheckpoint(
                        workflow_id=workflow_id,
                        current_step=i + 1,  # Next step to resume from
                        state=WorkflowState.PAUSED,
                        context_data={'data': context.data, 'request': context.request},
                        metadata={'paused_at_step': step.__name__}
                    )
                    await self.checkpoint_repo.save(pause_checkpoint)
                raise
            except Exception as e:
                if self.checkpoint_repo:
                    error_checkpoint = WorkflowCheckpoint(
                        workflow_id=workflow_id,
                        current_step=i,
                        state=WorkflowState.FAILED,
                        context_data={'data': context.data},
                        metadata={'error': str(e)}
                    )
                    await self.checkpoint_repo.save(error_checkpoint)
                raise e
        
        # Mark as completed
        if self.checkpoint_repo:
            await self.checkpoint_repo.delete(workflow_id)
        
        return context
    
    async def _execute_step(self, step: Callable, context: WorkflowContext) -> WorkflowContext:
        # Simulate realistic processing time
        await asyncio.sleep(2)  # 2 seconds per step
        return step(context)