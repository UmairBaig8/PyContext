from domain.entities import WorkflowContext

# Financial Risk Assessment Pipeline
def credit_data_collection_step(context: WorkflowContext) -> WorkflowContext:
    """Collect credit history and financial data"""
    customer_id = context.request.get('customer_id', 'unknown')
    context.data['credit_score'] = 750
    context.data['income_verified'] = True
    context.data['employment_history'] = '5_years'
    context.data['debt_to_income'] = 0.3
    return context

def risk_calculation_step(context: WorkflowContext) -> WorkflowContext:
    """Calculate risk scores using financial algorithms"""
    credit_score = context.data.get('credit_score', 600)
    dti_ratio = context.data.get('debt_to_income', 0.5)
    
    # Simple risk calculation
    risk_score = (credit_score / 850) * 0.7 + (1 - dti_ratio) * 0.3
    context.data['risk_score'] = round(risk_score, 3)
    context.data['risk_category'] = 'low' if risk_score > 0.7 else 'medium' if risk_score > 0.4 else 'high'
    return context

def compliance_check_step(context: WorkflowContext) -> WorkflowContext:
    """Verify regulatory compliance and KYC"""
    context.data['kyc_verified'] = True
    context.data['aml_cleared'] = True
    context.data['regulatory_flags'] = []
    context.data['compliance_status'] = 'approved'
    return context

def loan_decision_step(context: WorkflowContext) -> WorkflowContext:
    """Make final loan approval decision"""
    risk_category = context.data.get('risk_category', 'high')
    compliance_status = context.data.get('compliance_status', 'pending')
    
    if risk_category == 'low' and compliance_status == 'approved':
        context.data['loan_decision'] = 'approved'
        context.data['interest_rate'] = 3.5
        context.data['loan_amount'] = context.request.get('requested_amount', 100000)
    else:
        context.data['loan_decision'] = 'rejected'
        context.data['rejection_reason'] = f'Risk: {risk_category}, Compliance: {compliance_status}'
    
    return context

def notification_dispatch_step(context: WorkflowContext) -> WorkflowContext:
    """Send decision notification to customer"""
    decision = context.data.get('loan_decision', 'pending')
    context.data['notification_sent'] = True
    context.data['notification_method'] = 'email_sms'
    context.data['customer_notified_at'] = 'now'
    return context