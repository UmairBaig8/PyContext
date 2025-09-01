# Contributing to PyContext

We welcome contributions to PyContext! This document provides guidelines for contributing to the project.

## 🚀 Getting Started

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/yourusername/pycontext.git
   cd pycontext
   ```
3. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   pip install -e ".[dev]"
   ```

## 🏗️ Development Setup

### Code Style
We use Black for code formatting and Flake8 for linting:
```bash
black .
flake8 .
```

### Type Checking
We use MyPy for type checking:
```bash
mypy .
```

### Testing
Run tests with pytest:
```bash
pytest
```

## 📝 Making Changes

1. Create a new branch for your feature:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes following our coding standards:
   - Follow PEP 8 style guidelines
   - Add type hints to all functions
   - Write docstrings for public methods
   - Keep functions focused and small

3. Add tests for your changes:
   - Unit tests for new functionality
   - Integration tests for workflow scenarios
   - Ensure all tests pass

4. Update documentation if needed:
   - Update README.md for new features
   - Add docstrings to new classes/methods
   - Update examples if applicable

## 🎯 Contribution Areas

### High Priority
- Performance optimizations
- Additional workflow examples
- Better error handling
- Documentation improvements

### Medium Priority
- New checkpoint storage backends
- Monitoring and metrics
- Workflow visualization tools
- CLI improvements

### Low Priority
- Additional message queue adapters
- Web UI for workflow management
- Advanced scheduling features

## 📋 Pull Request Process

1. Ensure your code follows the style guidelines
2. Add or update tests as appropriate
3. Update documentation for any new features
4. Ensure all tests pass
5. Create a pull request with:
   - Clear title and description
   - Reference any related issues
   - Include screenshots for UI changes

## 🐛 Bug Reports

When reporting bugs, please include:
- Python version
- Operating system
- Steps to reproduce
- Expected vs actual behavior
- Error messages/stack traces

## 💡 Feature Requests

For new features, please:
- Check existing issues first
- Describe the use case
- Explain why it would be valuable
- Consider implementation complexity

## 📚 Code Organization

### Domain Layer (`domain/`)
- Core business entities
- Repository interfaces
- Domain-specific enums and types

### Infrastructure Layer (`infrastructure/`)
- Database implementations
- External system integrations
- Concrete repository implementations

### Services Layer (`services/`)
- Business logic
- Workflow orchestration
- Message queue management

### Application Layer (`application/`)
- Workflow step implementations
- Use case specific logic
- Domain workflows

## 🔍 Code Review Guidelines

### For Reviewers
- Check for code clarity and maintainability
- Verify test coverage
- Ensure documentation is updated
- Test the changes locally

### For Contributors
- Respond to feedback promptly
- Make requested changes
- Keep discussions focused and professional
- Update your branch with latest main

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

## 🤝 Community

- Be respectful and inclusive
- Help others learn and grow
- Share knowledge and best practices
- Celebrate contributions of all sizes

## 📞 Getting Help

- Open an issue for bugs or questions
- Start discussions for design decisions
- Reach out to maintainers for guidance

Thank you for contributing to PyContext! 🎉