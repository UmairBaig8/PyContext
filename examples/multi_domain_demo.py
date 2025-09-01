import asyncio
import logging
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from domain.entities import WorkflowContext, WorkflowMessage, Priority
from infrastructure.persistence import SQLiteCheckpointRepository
from services.workflow_engine import WorkflowEngine
from services.message_queue import WorkflowMessageQueue

# Import all workflow steps
from application.ml_workflows import (
    data_preprocessing_step, feature_engineering_step, model_training_step,
    model_evaluation_step, model_deployment_step
)
from application.financial_workflows import (
    credit_data_collection_step, risk_calculation_step, compliance_check_step,
    loan_decision_step, notification_dispatch_step
)
from application.ecommerce_workflows import (
    inventory_check_step, payment_processing_step, shipping_calculation_step,
    order_fulfillment_step, customer_notification_step,
    transaction_analysis_step, ml_fraud_scoring_step, manual_review_step
)
from application.healthcare_workflows import (
    patient_data_ingestion_step, symptom_analysis_step, diagnostic_imaging_step,
    treatment_recommendation_step, prescription_generation_step
)

async def multi_domain_demo():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
    logger = logging.getLogger('workflow')
    
    print("🌐 MULTI-DOMAIN WORKFLOW DEMONSTRATION")
    print("=" * 60)
    
    # Infrastructure
    checkpoint_repo = SQLiteCheckpointRepository("multi_domain_checkpoints.db")
    mq = WorkflowMessageQueue(preemptive=True, checkpoint_repo=checkpoint_repo)
    
    # Configure ML Pipeline (5 steps × 2s = 10s)
    ml_engine = WorkflowEngine(checkpoint_repo)
    ml_engine.configure('ml-pipeline', [
        data_preprocessing_step, feature_engineering_step, model_training_step,
        model_evaluation_step, model_deployment_step
    ])
    
    # Configure Financial Risk Assessment (5 steps × 2s = 10s)
    financial_engine = WorkflowEngine(checkpoint_repo)
    financial_engine.configure('loan-processing', [
        credit_data_collection_step, risk_calculation_step, compliance_check_step,
        loan_decision_step, notification_dispatch_step
    ])
    
    # Configure E-commerce Order Processing (5 steps × 2s = 10s)
    ecommerce_engine = WorkflowEngine(checkpoint_repo)
    ecommerce_engine.configure('order-processing', [
        inventory_check_step, payment_processing_step, shipping_calculation_step,
        order_fulfillment_step, customer_notification_step
    ])
    
    # Configure Fraud Detection (3 steps × 2s = 6s)
    fraud_engine = WorkflowEngine(checkpoint_repo)
    fraud_engine.configure('fraud-detection', [
        transaction_analysis_step, ml_fraud_scoring_step, manual_review_step
    ])
    
    # Configure Healthcare Diagnosis (5 steps × 2s = 10s)
    healthcare_engine = WorkflowEngine(checkpoint_repo)
    healthcare_engine.configure('medical-diagnosis', [
        patient_data_ingestion_step, symptom_analysis_step, diagnostic_imaging_step,
        treatment_recommendation_step, prescription_generation_step
    ])
    
    # Register all workflows
    mq.register_workflow('ml-pipeline', ml_engine)
    mq.register_workflow('loan-processing', financial_engine)
    mq.register_workflow('order-processing', ecommerce_engine)
    mq.register_workflow('fraud-detection', fraud_engine)
    mq.register_workflow('medical-diagnosis', healthcare_engine)
    
    # Start consumer
    consumer_task = asyncio.create_task(mq.start_consumer())
    
    # Scenario 1: Start long-running ML training
    print("🤖 Starting ML model training pipeline (10 seconds)")
    await mq.publish(WorkflowMessage(
        priority=Priority.LOW,
        workflow_name='ml-pipeline',
        context=WorkflowContext.create(
            logger=logger,
            request={'dataset': 'customer_churn', 'algorithm': 'gradient_boosting'}
        )
    ))
    
    # Let it run for 5 seconds (2.5 steps completed)
    await asyncio.sleep(5)
    
    # Scenario 2: URGENT - Fraud detection needed
    print("\n🚨 URGENT: Suspicious transaction detected - Interrupting ML training")
    await mq.publish(WorkflowMessage(
        priority=Priority.HIGH,
        workflow_name='fraud-detection',
        context=WorkflowContext.create(
            logger=logger,
            request={'total_amount': 5000, 'customer_history': {'avg_transaction': 100}}
        )
    ))
    
    # Let fraud detection complete and ML resume
    await asyncio.sleep(8)
    
    # Scenario 3: Medical emergency
    print("\n🏥 URGENT: Medical diagnosis required")
    await mq.publish(WorkflowMessage(
        priority=Priority.HIGH,
        workflow_name='medical-diagnosis',
        context=WorkflowContext.create(
            logger=logger,
            request={'patient_id': 'PAT_67890', 'symptoms': ['chest_pain', 'shortness_of_breath']}
        )
    ))
    
    # Scenario 4: Regular e-commerce order
    print("🛒 Processing e-commerce order")
    await mq.publish(WorkflowMessage(
        priority=Priority.MEDIUM,
        workflow_name='order-processing',
        context=WorkflowContext.create(
            logger=logger,
            request={'items': ['laptop', 'mouse'], 'total_amount': 1200}
        )
    ))
    
    # Let everything complete
    await asyncio.sleep(25)
    
    mq.stop()
    consumer_task.cancel()
    
    print("\n✅ MULTI-DOMAIN DEMO COMPLETE")
    print("📊 Demonstrated workflows:")
    print("   • 🤖 ML Pipeline (data → features → training → evaluation → deployment)")
    print("   • 💰 Financial Risk (credit → risk → compliance → decision → notify)")
    print("   • 🛒 E-commerce Order (inventory → payment → shipping → fulfillment → notify)")
    print("   • 🚨 Fraud Detection (analysis → ML scoring → manual review)")
    print("   • 🏥 Healthcare Diagnosis (data → symptoms → imaging → treatment → prescription)")

if __name__ == "__main__":
    asyncio.run(multi_domain_demo())