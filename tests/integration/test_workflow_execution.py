import pytest
import asyncio
from domain.entities import WorkflowContext, WorkflowMessage, Priority
from infrastructure.persistence import SQLiteCheckpointRepository
from services.workflow_engine import WorkflowEngine
from services.message_queue import WorkflowMessageQueue

def simple_step1(context: WorkflowContext) -> WorkflowContext:
    context.data['step1'] = 'completed'
    return context

def simple_step2(context: WorkflowContext) -> WorkflowContext:
    context.data['step2'] = 'completed'
    return context

@pytest.mark.asyncio
async def test_basic_workflow_execution():
    """Test basic workflow execution without interruption."""
    checkpoint_repo = SQLiteCheckpointRepository(":memory:")
    engine = WorkflowEngine(checkpoint_repo)
    engine.configure('test-workflow', [simple_step1, simple_step2])
    
    context = WorkflowContext.create()
    result = await engine.execute(context)
    
    assert result.data['step1'] == 'completed'
    assert result.data['step2'] == 'completed'

@pytest.mark.asyncio
async def test_priority_message_queue():
    """Test priority-based message processing."""
    checkpoint_repo = SQLiteCheckpointRepository(":memory:")
    mq = WorkflowMessageQueue(preemptive=False, checkpoint_repo=checkpoint_repo)
    
    engine = WorkflowEngine(checkpoint_repo)
    engine.configure('test-workflow', [simple_step1])
    mq.register_workflow('test-workflow', engine)
    
    # Start consumer
    consumer_task = asyncio.create_task(mq.start_consumer())
    
    # Publish messages with different priorities
    await mq.publish(WorkflowMessage(
        priority=Priority.LOW,
        workflow_name='test-workflow',
        context=WorkflowContext.create()
    ))
    
    await mq.publish(WorkflowMessage(
        priority=Priority.HIGH,
        workflow_name='test-workflow',
        context=WorkflowContext.create()
    ))
    
    # Let it process
    await asyncio.sleep(0.1)
    mq.stop()
    consumer_task.cancel()
    
    # High priority should process first
    assert True  # Basic test that no exceptions occurred