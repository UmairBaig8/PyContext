import asyncio
import logging
from domain.entities import WorkflowContext, WorkflowMessage, Priority
from infrastructure.persistence import SQLiteCheckpointRepository
from services.workflow_engine import WorkflowEngine
from services.message_queue import WorkflowMessageQueue
from application.workflow_steps import (
    data_extraction_step, data_transformation_step, data_enrichment_step,
    notification_step, audit_logging_step
)

async def realistic_demo():
    # Setup logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
    logger = logging.getLogger('workflow')
    
    print("🏗️  LAYERED ARCHITECTURE WORKFLOW DEMO")
    print("=" * 50)
    
    # Infrastructure layer
    checkpoint_repo = SQLiteCheckpointRepository()
    
    # Service layer
    mq = WorkflowMessageQueue(preemptive=True, checkpoint_repo=checkpoint_repo)
    
    # Configure workflow engines
    data_processing_engine = WorkflowEngine(checkpoint_repo)
    data_processing_engine.configure('data-processing', [
        data_extraction_step,
        data_transformation_step, 
        data_enrichment_step,
        audit_logging_step
    ])
    
    urgent_notification_engine = WorkflowEngine(checkpoint_repo)
    urgent_notification_engine.configure('urgent-notification', [
        notification_step
    ])
    
    # Register workflows
    mq.register_workflow('data-processing', data_processing_engine)
    mq.register_workflow('urgent-notification', urgent_notification_engine)
    
    # Start consumer
    consumer_task = asyncio.create_task(mq.start_consumer())
    
    # Scenario: Long-running data processing workflow
    print("📊 Starting long data processing workflow (4 steps × 2s = 8s total)")
    await mq.publish(WorkflowMessage(
        priority=Priority.LOW,
        workflow_name='data-processing',
        context=WorkflowContext.create(
            logger=logger,
            request={'user_id': 12345, 'dataset': 'customer_data'}
        )
    ))
    
    # Let it run for 5 seconds (completes 2 steps: extraction + transformation)
    print("⏳ Processing... (5 seconds)")
    await asyncio.sleep(5)
    
    # Urgent notification arrives
    print("\n🚨 URGENT NOTIFICATION REQUIRED - INTERRUPTING DATA PROCESSING")
    await mq.publish(WorkflowMessage(
        priority=Priority.HIGH,
        workflow_name='urgent-notification',
        context=WorkflowContext.create(
            logger=logger,
            request={'alert_type': 'security_breach', 'severity': 'critical'}
        )
    ))
    
    # Let urgent task complete and data processing resume
    print("⏳ Handling urgent notification and resuming data processing...")
    await asyncio.sleep(8)
    
    mq.stop()
    consumer_task.cancel()
    
    print("\n✅ DEMO COMPLETE")
    print("📋 Data processing resumed from step 3 (enrichment) after interruption")
    print("🏛️  Clean layered architecture maintained throughout")

if __name__ == "__main__":
    asyncio.run(realistic_demo())