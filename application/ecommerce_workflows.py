from domain.entities import WorkflowContext

# E-commerce Order Processing Pipeline
def inventory_check_step(context: WorkflowContext) -> WorkflowContext:
    """Check product availability and reserve inventory"""
    order_items = context.request.get('items', [])
    context.data['inventory_reserved'] = True
    context.data['available_items'] = len(order_items)
    context.data['warehouse_location'] = 'US_EAST'
    return context

def payment_processing_step(context: WorkflowContext) -> WorkflowContext:
    """Process customer payment and handle transactions"""
    payment_method = context.request.get('payment_method', 'credit_card')
    amount = context.request.get('total_amount', 0)
    
    context.data['payment_processed'] = True
    context.data['transaction_id'] = f'txn_{hash(str(amount))}'
    context.data['payment_status'] = 'completed'
    context.data['charged_amount'] = amount
    return context

def shipping_calculation_step(context: WorkflowContext) -> WorkflowContext:
    """Calculate shipping costs and delivery estimates"""
    shipping_address = context.request.get('shipping_address', {})
    context.data['shipping_cost'] = 15.99
    context.data['estimated_delivery'] = '3-5_business_days'
    context.data['shipping_carrier'] = 'FedEx'
    context.data['tracking_number'] = f'FX{hash(str(shipping_address))}'
    return context

def order_fulfillment_step(context: WorkflowContext) -> WorkflowContext:
    """Prepare order for shipment and generate labels"""
    context.data['picking_list_generated'] = True
    context.data['shipping_label_created'] = True
    context.data['order_status'] = 'ready_to_ship'
    context.data['fulfillment_center'] = context.data.get('warehouse_location', 'default')
    return context

def customer_notification_step(context: WorkflowContext) -> WorkflowContext:
    """Send order confirmation and tracking info to customer"""
    tracking_number = context.data.get('tracking_number', 'unknown')
    context.data['confirmation_email_sent'] = True
    context.data['tracking_sms_sent'] = True
    context.data['customer_portal_updated'] = True
    return context

# Fraud Detection Pipeline
def transaction_analysis_step(context: WorkflowContext) -> WorkflowContext:
    """Analyze transaction patterns for fraud indicators"""
    amount = context.request.get('total_amount', 0)
    customer_history = context.request.get('customer_history', {})
    
    context.data['transaction_score'] = 0.85 if amount < 1000 else 0.45
    context.data['velocity_check'] = 'passed'
    context.data['geo_location_match'] = True
    return context

def ml_fraud_scoring_step(context: WorkflowContext) -> WorkflowContext:
    """Apply ML models for fraud detection"""
    transaction_score = context.data.get('transaction_score', 0.5)
    context.data['ml_fraud_score'] = transaction_score * 0.9
    context.data['fraud_probability'] = 'low' if transaction_score > 0.7 else 'high'
    context.data['model_version'] = 'fraud_detector_v2.1'
    return context

def manual_review_step(context: WorkflowContext) -> WorkflowContext:
    """Queue high-risk transactions for manual review"""
    fraud_probability = context.data.get('fraud_probability', 'medium')
    
    if fraud_probability == 'high':
        context.data['manual_review_required'] = True
        context.data['review_queue'] = 'high_priority'
        context.data['estimated_review_time'] = '2_hours'
    else:
        context.data['auto_approved'] = True
        context.data['manual_review_required'] = False
    
    return context