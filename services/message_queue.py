import asyncio
import heapq
from typing import Dict
from domain.entities import WorkflowMessage
from domain.repositories import CheckpointRepository
from .workflow_engine import WorkflowEngine

class WorkflowMessageQueue:
    def __init__(self, preemptive: bool = False, checkpoint_repo: CheckpointRepository = None):
        self.queue = []
        self.engines: Dict[str, WorkflowEngine] = {}
        self.running = False
        self.preemptive = preemptive
        self.checkpoint_repo = checkpoint_repo
        self.current_task = None
    
    def register_workflow(self, name: str, engine: WorkflowEngine):
        self.engines[name] = engine
    
    async def publish(self, message: WorkflowMessage):
        heapq.heappush(self.queue, message)
        
        # Preemptive interruption for high priority
        if (self.preemptive and message.priority.value == 1 and 
            self.current_task and not self.current_task.done()):
            if message.context.logger:
                message.context.logger.warning("🚨 HIGH PRIORITY - Interrupting current workflow")
            self.current_task.cancel()
    
    async def start_consumer(self):
        self.running = True
        while self.running:
            if self.queue:
                message = heapq.heappop(self.queue)
                self.current_task = asyncio.create_task(self._process_message(message))
                try:
                    await self.current_task
                except asyncio.CancelledError:
                    # Re-queue interrupted message
                    heapq.heappush(self.queue, message)
                    if message.context.logger:
                        message.context.logger.info(f"📋 Workflow {message.workflow_name} paused and re-queued")
            else:
                await asyncio.sleep(0.1)
    
    async def _process_message(self, message: WorkflowMessage):
        engine = self.engines.get(message.workflow_name)
        if engine:
            try:
                await engine.execute(message.context)
                if message.context.logger:
                    message.context.logger.info(f"✅ Completed {message.workflow_name} (Priority: {message.priority.name})")
            except asyncio.CancelledError:
                raise  # Re-raise to handle in consumer
            except Exception as e:
                if message.context.logger:
                    # Sanitize workflow name to prevent log injection
                    safe_name = message.workflow_name.replace('\n', '').replace('\r', '')
                    message.context.logger.error(f"❌ Failed {safe_name}: {e}")
        else:
            if message.context.logger:
                safe_name = message.workflow_name.replace('\n', '').replace('\r', '')
                message.context.logger.error(f"⚠️ Workflow '{safe_name}' not registered")
    
    def stop(self):
        self.running = False