# PyContext - Dynamic Workflow Engine

A professional, production-ready workflow engine with priority-based execution, checkpoint resumption, and layered architecture.

## 🚀 Features

- **Priority-based Execution**: HIGH priority workflows can interrupt running tasks
- **Checkpoint Resumption**: Workflows resume from last completed step after interruption
- **Layered Architecture**: Clean separation following Domain-Driven Design principles
- **Multi-Domain Support**: ML, Financial, E-commerce, Healthcare workflow examples
- **Async Processing**: Non-blocking workflow execution
- **Persistent State**: SQLite-based checkpoint storage
- **Professional Structure**: Production-ready codebase

## 📋 Quick Start

### Installation

```bash
git clone https://github.com/yourusername/pycontext.git
cd pycontext
pip install -r requirements.txt
```

### Basic Usage

```python
import asyncio
from domain.entities import WorkflowContext, WorkflowMessage, Priority
from infrastructure.persistence import SQLiteCheckpointRepository
from services.workflow_engine import WorkflowEngine
from services.message_queue import WorkflowMessageQueue

# Setup
checkpoint_repo = SQLiteCheckpointRepository()
mq = WorkflowMessageQueue(preemptive=True, checkpoint_repo=checkpoint_repo)

# Configure workflow
engine = WorkflowEngine(checkpoint_repo)
engine.configure('data-processing', [step1, step2, step3])
mq.register_workflow('data-processing', engine)

# Execute
await mq.publish(WorkflowMessage(
    priority=Priority.HIGH,
    workflow_name='data-processing',
    context=WorkflowContext.create(request={'user_id': 123})
))
```

## 🏗️ Architecture

```
├── domain/           # Core business entities and interfaces
├── infrastructure/   # Database and external systems
├── services/         # Business logic and orchestration  
├── application/      # Workflow steps and use cases
└── examples/         # Demonstrations and samples
```

### Domain Layer
- **Entities**: `WorkflowContext`, `WorkflowCheckpoint`, `WorkflowMessage`
- **Repositories**: Abstract interfaces for data persistence
- **Enums**: `Priority`, `WorkflowState`

### Infrastructure Layer
- **Persistence**: SQLite checkpoint repository implementation
- **External Systems**: Database connections, file systems

### Services Layer
- **WorkflowEngine**: Core execution logic with checkpoint support
- **MessageQueue**: Priority-based orchestration and preemption

### Application Layer
- **Workflow Steps**: Domain-specific business logic
- **Use Cases**: ML, Financial, E-commerce, Healthcare workflows

## 📊 Workflow Examples

### Machine Learning Pipeline
```python
from application.ml_workflows import (
    data_preprocessing_step, feature_engineering_step, 
    model_training_step, model_evaluation_step, model_deployment_step
)

ml_engine = WorkflowEngine(checkpoint_repo)
ml_engine.configure('ml-pipeline', [
    data_preprocessing_step, feature_engineering_step, model_training_step,
    model_evaluation_step, model_deployment_step
])
```

### Financial Risk Assessment
```python
from application.financial_workflows import (
    credit_data_collection_step, risk_calculation_step, 
    compliance_check_step, loan_decision_step
)

financial_engine = WorkflowEngine(checkpoint_repo)
financial_engine.configure('loan-processing', [
    credit_data_collection_step, risk_calculation_step,
    compliance_check_step, loan_decision_step
])
```

## 🎯 Priority System

- **HIGH (1)**: Critical tasks that interrupt running workflows
- **MEDIUM (2)**: Important tasks processed in order
- **LOW (3)**: Background tasks with lowest priority

## 💾 Checkpoint System

Workflows automatically save progress and can resume from interruption:

```python
# Workflow interrupted at step 2
# Automatically resumes from step 3 when re-queued
# No duplicate work performed
```

## 🔧 Configuration

### Preemptive Mode
```python
# Enable interruption for high-priority tasks
mq = WorkflowMessageQueue(preemptive=True, checkpoint_repo=checkpoint_repo)
```

### Custom Database
```python
# Use custom database path
checkpoint_repo = SQLiteCheckpointRepository("custom_checkpoints.db")
```

## 📈 Performance

- **Async Execution**: Non-blocking workflow processing
- **Efficient Queuing**: Priority heap for O(log n) operations
- **Minimal Overhead**: Lightweight checkpoint storage
- **Scalable Design**: Supports thousands of concurrent workflows

## 🧪 Running Examples

### Basic Demo
```bash
python main_layered.py
```

### Multi-Domain Demo
```bash
python examples/multi_domain_demo.py
```

### Expected Output
```
🌐 MULTI-DOMAIN WORKFLOW DEMONSTRATION
============================================================
🤖 Starting ML model training pipeline (10 seconds)
2025-09-02 01:02:25,243 - [ml-pipeline] Starting step 0: data_preprocessing_step
2025-09-02 01:02:27,245 - [ml-pipeline] Completed step 0: data_preprocessing_step
2025-09-02 01:02:27,248 - [ml-pipeline] Starting step 1: feature_engineering_step
2025-09-02 01:02:29,250 - [ml-pipeline] Completed step 1: feature_engineering_step
2025-09-02 01:02:29,253 - [ml-pipeline] Starting step 2: model_training_step

🚨 URGENT: Suspicious transaction detected - Interrupting ML training
2025-09-02 01:02:30,241 - 🚨 HIGH PRIORITY - Interrupting current workflow
2025-09-02 01:02:30,245 - 📋 Workflow ml-pipeline paused and re-queued
2025-09-02 01:02:30,248 - [fraud-detection] Starting step 0: transaction_analysis_step
2025-09-02 01:02:32,249 - [fraud-detection] Completed step 0: transaction_analysis_step
2025-09-02 01:02:32,253 - [fraud-detection] Starting step 1: ml_fraud_scoring_step
2025-09-02 01:02:34,254 - [fraud-detection] Completed step 1: ml_fraud_scoring_step
2025-09-02 01:02:34,257 - [fraud-detection] Starting step 2: manual_review_step
2025-09-02 01:02:36,259 - [fraud-detection] Completed step 2: manual_review_step
2025-09-02 01:02:36,260 - ✅ Completed fraud-detection (Priority: HIGH)
2025-09-02 01:02:36,260 - [ml-pipeline] Resuming from step 3
2025-09-02 01:02:36,261 - [ml-pipeline] Starting step 3: model_evaluation_step

🏥 URGENT: Medical diagnosis required
2025-09-02 01:02:38,244 - 🚨 HIGH PRIORITY - Interrupting current workflow
🛒 Processing e-commerce order
2025-09-02 01:02:38,247 - 📋 Workflow ml-pipeline paused and re-queued
2025-09-02 01:02:38,249 - [medical-diagnosis] Starting step 0: patient_data_ingestion_step
2025-09-02 01:02:40,250 - [medical-diagnosis] Completed step 0: patient_data_ingestion_step
2025-09-02 01:02:40,253 - [medical-diagnosis] Starting step 1: symptom_analysis_step
2025-09-02 01:02:42,255 - [medical-diagnosis] Completed step 1: symptom_analysis_step
2025-09-02 01:02:42,257 - [medical-diagnosis] Starting step 2: diagnostic_imaging_step
2025-09-02 01:02:44,258 - [medical-diagnosis] Completed step 2: diagnostic_imaging_step
2025-09-02 01:02:44,261 - [medical-diagnosis] Starting step 3: treatment_recommendation_step
2025-09-02 01:02:46,262 - [medical-diagnosis] Completed step 3: treatment_recommendation_step
2025-09-02 01:02:46,263 - [medical-diagnosis] Starting step 4: prescription_generation_step
2025-09-02 01:02:48,265 - [medical-diagnosis] Completed step 4: prescription_generation_step
2025-09-02 01:02:48,269 - ✅ Completed medical-diagnosis (Priority: HIGH)
2025-09-02 01:02:48,272 - [order-processing] Starting step 0: inventory_check_step
2025-09-02 01:02:50,273 - [order-processing] Completed step 0: inventory_check_step
2025-09-02 01:02:50,278 - [order-processing] Starting step 1: payment_processing_step
2025-09-02 01:02:52,280 - [order-processing] Completed step 1: payment_processing_step
2025-09-02 01:02:52,284 - [order-processing] Starting step 2: shipping_calculation_step
2025-09-02 01:02:54,286 - [order-processing] Completed step 2: shipping_calculation_step
2025-09-02 01:02:54,290 - [order-processing] Starting step 3: order_fulfillment_step
2025-09-02 01:02:56,292 - [order-processing] Completed step 3: order_fulfillment_step
2025-09-02 01:02:56,294 - [order-processing] Starting step 4: customer_notification_step
2025-09-02 01:02:58,295 - [order-processing] Completed step 4: customer_notification_step
2025-09-02 01:02:58,299 - ✅ Completed order-processing (Priority: MEDIUM)
2025-09-02 01:02:58,300 - [ml-pipeline] Resuming from step 4
2025-09-02 01:02:58,302 - [ml-pipeline] Starting step 4: model_deployment_step
2025-09-02 01:03:00,303 - [ml-pipeline] Completed step 4: model_deployment_step
2025-09-02 01:03:00,308 - ✅ Completed ml-pipeline (Priority: LOW)

✅ MULTI-DOMAIN DEMO COMPLETE
📊 Demonstrated workflows:
   • 🤖 ML Pipeline (data → features → training → evaluation → deployment)
   • 💰 Financial Risk (credit → risk → compliance → decision → notify)
   • 🛒 E-commerce Order (inventory → payment → shipping → fulfillment → notify)
   • 🚨 Fraud Detection (analysis → ML scoring → manual review)
   • 🏥 Healthcare Diagnosis (data → symptoms → imaging → treatment → prescription)
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🏆 Use Cases

- **Machine Learning**: Model training pipelines with checkpoints
- **Financial Services**: Risk assessment and loan processing
- **E-commerce**: Order processing and fraud detection
- **Healthcare**: Medical diagnosis and clinical trials
- **Data Processing**: ETL pipelines with resumable execution
- **Microservices**: Orchestration with priority handling

## 📚 Documentation

For detailed documentation, see the [docs](docs/) directory.

## 🐛 Issues

Found a bug? Please open an issue on [GitHub Issues](https://github.com/yourusername/pycontext/issues).

## ⭐ Support

If you find this project helpful, please give it a star on GitHub!