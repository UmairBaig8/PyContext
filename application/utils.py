import uuid
import hashlib
from datetime import datetime

def generate_secure_id(prefix: str = "") -> str:
    """Generate a secure, deterministic ID using UUID4."""
    return f"{prefix}{uuid.uuid4().hex[:8]}" if prefix else uuid.uuid4().hex[:8]

def generate_deterministic_id(input_str: str, prefix: str = "") -> str:
    """Generate a deterministic ID using SHA256 hash."""
    hash_obj = hashlib.sha256(input_str.encode())
    hash_hex = hash_obj.hexdigest()[:8]
    return f"{prefix}{hash_hex}" if prefix else hash_hex

def get_current_timestamp() -> str:
    """Get current timestamp in ISO format."""
    return datetime.now().isoformat()

def validate_numeric_input(value, field_name: str, default=0):
    """Validate numeric input with proper error handling."""
    if value is None:
        return default
    
    if isinstance(value, (int, float)):
        return value
    
    try:
        return float(value)
    except (ValueError, TypeError):
        raise ValueError(f"Invalid {field_name}: expected numeric value, got {type(value).__name__}")

def sanitize_log_input(text: str) -> str:
    """Sanitize text for safe logging by removing newlines and control characters."""
    if not isinstance(text, str):
        text = str(text)
    return text.replace('\n', '').replace('\r', '').replace('\t', ' ')