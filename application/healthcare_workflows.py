from domain.entities import WorkflowContext

# Medical Diagnosis Pipeline
def patient_data_ingestion_step(context: WorkflowContext) -> WorkflowContext:
    """Collect and validate patient medical data"""
    patient_id = context.request.get('patient_id', 'unknown')
    context.data['medical_history'] = 'collected'
    context.data['vital_signs'] = {'bp': '120/80', 'hr': 72, 'temp': 98.6}
    context.data['lab_results'] = 'pending'
    context.data['patient_consent'] = True
    return context

def symptom_analysis_step(context: WorkflowContext) -> WorkflowContext:
    """Analyze reported symptoms and medical history"""
    symptoms = context.request.get('symptoms', [])
    context.data['symptom_severity'] = 'moderate'
    context.data['symptom_duration'] = '3_days'
    context.data['differential_diagnosis'] = ['condition_a', 'condition_b', 'condition_c']
    context.data['risk_factors'] = ['age', 'family_history']
    return context

def diagnostic_imaging_step(context: WorkflowContext) -> WorkflowContext:
    """Process medical imaging and radiology results"""
    imaging_type = context.request.get('imaging_type', 'xray')
    context.data['imaging_completed'] = True
    context.data['imaging_findings'] = 'normal_with_minor_abnormalities'
    context.data['radiologist_review'] = 'completed'
    context.data['imaging_report_id'] = f'IMG_{hash(imaging_type)}'
    return context

def treatment_recommendation_step(context: WorkflowContext) -> WorkflowContext:
    """Generate treatment recommendations based on diagnosis"""
    diagnosis = context.data.get('differential_diagnosis', [])
    context.data['recommended_treatment'] = 'medication_therapy'
    context.data['medication_list'] = ['med_a_10mg', 'med_b_5mg']
    context.data['follow_up_required'] = True
    context.data['follow_up_timeline'] = '2_weeks'
    return context

def prescription_generation_step(context: WorkflowContext) -> WorkflowContext:
    """Generate electronic prescriptions and send to pharmacy"""
    medications = context.data.get('medication_list', [])
    context.data['prescription_id'] = f'RX_{hash(str(medications))}'
    context.data['pharmacy_notified'] = True
    context.data['drug_interaction_check'] = 'passed'
    context.data['insurance_verification'] = 'approved'
    return context

# Clinical Trial Enrollment Pipeline
def eligibility_screening_step(context: WorkflowContext) -> WorkflowContext:
    """Screen patient eligibility for clinical trials"""
    age = context.request.get('age', 0)
    medical_conditions = context.request.get('conditions', [])
    
    context.data['age_eligible'] = 18 <= age <= 75
    context.data['condition_match'] = len(medical_conditions) > 0
    context.data['exclusion_criteria_met'] = False
    context.data['preliminary_eligible'] = context.data['age_eligible'] and context.data['condition_match']
    return context

def informed_consent_step(context: WorkflowContext) -> WorkflowContext:
    """Process informed consent documentation"""
    context.data['consent_form_provided'] = True
    context.data['risks_explained'] = True
    context.data['patient_questions_answered'] = True
    context.data['consent_signed'] = True
    context.data['consent_date'] = 'today'
    return context

def baseline_assessment_step(context: WorkflowContext) -> WorkflowContext:
    """Conduct baseline medical assessments"""
    context.data['baseline_vitals'] = {'bp': '118/78', 'weight': '70kg', 'height': '175cm'}
    context.data['baseline_labs'] = 'collected'
    context.data['quality_of_life_survey'] = 'completed'
    context.data['baseline_imaging'] = 'scheduled'
    return context

def randomization_step(context: WorkflowContext) -> WorkflowContext:
    """Randomize patient to treatment or control group"""
    import random
    treatment_group = 'treatment' if random.random() > 0.5 else 'control'
    
    context.data['randomization_completed'] = True
    context.data['treatment_group'] = treatment_group
    context.data['study_drug_assigned'] = f'drug_{treatment_group}'
    context.data['randomization_date'] = 'today'
    return context