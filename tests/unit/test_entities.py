import pytest
from domain.entities import WorkflowContext, WorkflowCheckpoint, WorkflowState, Priority

def test_workflow_context_creation():
    """Test WorkflowContext creation and basic functionality."""
    context = WorkflowContext.create(request={'user_id': 123})
    
    assert context.id is not None
    assert context.data == {}
    assert context.request == {'user_id': 123}
    assert context.logger is None

def test_workflow_checkpoint():
    """Test WorkflowCheckpoint creation."""
    checkpoint = WorkflowCheckpoint(
        workflow_id='test-123',
        current_step=2,
        state=WorkflowState.RUNNING,
        context_data={'data': {'step1': 'completed'}},
        metadata={'step_name': 'test_step'}
    )
    
    assert checkpoint.workflow_id == 'test-123'
    assert checkpoint.current_step == 2
    assert checkpoint.state == WorkflowState.RUNNING

def test_priority_ordering():
    """Test priority enum ordering."""
    assert Priority.HIGH.value < Priority.MEDIUM.value
    assert Priority.MEDIUM.value < Priority.LOW.value
    assert Priority.HIGH.value == 1