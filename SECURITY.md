# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |

## Reporting a Vulnerability

If you discover a security vulnerability in PyContext, please report it by emailing [security@pycontext.dev](mailto:security@pycontext.dev).

**Please do not report security vulnerabilities through public GitHub issues.**

### What to Include

- Description of the vulnerability
- Steps to reproduce the issue
- Potential impact
- Suggested fix (if available)

### Response Timeline

- **Initial Response**: Within 48 hours
- **Status Update**: Within 7 days
- **Fix Timeline**: Critical issues within 30 days

## Security Measures

### Input Validation
- All user inputs are validated and sanitized
- Numeric inputs are properly type-checked
- Log inputs are sanitized to prevent injection attacks

### Resource Management
- Database connections use context managers
- Proper cleanup of async resources
- Memory leak prevention

### ID Generation
- Secure UUID-based ID generation
- Deterministic hashing for tracking numbers
- No use of insecure hash() function

### Error Handling
- Comprehensive exception handling
- Secure error logging without sensitive data exposure
- Graceful degradation on failures

## Best Practices

1. **Never log sensitive data** (passwords, tokens, personal information)
2. **Validate all inputs** before processing
3. **Use secure random generators** for IDs and tokens
4. **Implement proper resource cleanup** in all code paths
5. **Sanitize log messages** to prevent injection attacks

## Dependencies

We regularly audit our dependencies for security vulnerabilities:
- Automated dependency scanning
- Regular updates to latest secure versions
- Minimal dependency footprint

## Deployment Security

### Production Recommendations
- Use environment variables for configuration
- Enable database encryption at rest
- Implement proper access controls
- Monitor for suspicious activity
- Regular security audits

### Configuration
```python
# Production configuration example
checkpoint_repo = SQLiteCheckpointRepository(
    db_path=os.getenv('DB_PATH', 'secure_location/checkpoints.db')
)

# Use zero delay in production
engine = WorkflowEngine(checkpoint_repo, step_delay=0.0)
```

## Contact

For security-related questions or concerns, contact:
- Email: [security@pycontext.dev](mailto:security@pycontext.dev)
- Security Team: [@pycontext-security](https://github.com/pycontext-security)

## Acknowledgments

We appreciate responsible disclosure of security vulnerabilities and will acknowledge contributors in our security advisories (with permission).