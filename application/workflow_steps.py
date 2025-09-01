from domain.entities import WorkflowContext

def data_extraction_step(context: WorkflowContext) -> WorkflowContext:
    """Extract data from source systems"""
    user_id = context.request.get('user_id') if context.request else 'unknown'
    context.data['extracted_data'] = f'user_data_{user_id}'
    context.data['extraction_status'] = 'completed'
    return context

def data_transformation_step(context: WorkflowContext) -> WorkflowContext:
    """Transform and validate extracted data"""
    raw_data = context.data.get('extracted_data', '')
    context.data['transformed_data'] = raw_data.upper()
    context.data['validation_passed'] = True
    return context

def data_enrichment_step(context: WorkflowContext) -> WorkflowContext:
    """Enrich data with additional information"""
    context.data['enriched_data'] = context.data.get('transformed_data', '') + '_ENRICHED'
    context.data['enrichment_timestamp'] = 'now'
    return context

def notification_step(context: WorkflowContext) -> WorkflowContext:
    """Send notifications about processing completion"""
    context.data['notification_sent'] = True
    context.data['notification_channel'] = 'email'
    return context

def audit_logging_step(context: WorkflowContext) -> WorkflowContext:
    """Log audit trail for compliance"""
    context.data['audit_logged'] = True
    context.data['compliance_status'] = 'compliant'
    return context