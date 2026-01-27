# Contributing to ScreenshotScanner

Thank you for your interest in contributing to ScreenshotScanner! This document provides guidelines for contributing to the project.

## Code of Conduct

Be respectful and constructive in all interactions. We're all here to make this project better!

## How to Contribute

### Reporting Bugs

If you find a bug, please create an issue on GitHub with:

- A clear, descriptive title
- Steps to reproduce the bug
- Expected behavior vs. actual behavior
- Screenshots or code samples if applicable
- Your environment (OS, Python version, package version)

### Suggesting Enhancements

We welcome suggestions for new features or improvements! Please create an issue with:

- A clear description of the enhancement
- Use cases and benefits
- Any implementation ideas you have

### Pull Requests

1. **Fork the repository** and create your branch from `main`
2. **Make your changes** with clear, descriptive commits
3. **Add tests** for new functionality
4. **Update documentation** if needed
5. **Ensure tests pass** before submitting
6. **Submit a pull request** with a clear description

## Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/ScreenshotScanner.git
cd ScreenshotScanner

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e .

# Install development dependencies
pip install pytest black flake8
```

## Code Style

- Follow PEP 8 guidelines
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Keep functions focused and modular

### Running Code Formatters

```bash
# Format code with black
black screenshot_scanner/

# Check code style
flake8 screenshot_scanner/
```

## Testing

```bash
# Run all tests
python -m pytest tests/

# Run with coverage
python -m pytest --cov=screenshot_scanner tests/
```

### Writing Tests

- Add tests for all new features
- Ensure edge cases are covered
- Use descriptive test names
- Keep tests independent and isolated

## Commit Messages

- Use clear, descriptive commit messages
- Start with a verb (Add, Fix, Update, Remove, etc.)
- Keep the first line under 50 characters
- Add detailed description if needed

Example:
```
Add support for PNG alpha channel detection

- Implement alpha channel check in detector
- Add test cases for RGBA images
- Update documentation
```

## Documentation

- Update README.md for user-facing changes
- Add docstrings for new functions/classes
- Include usage examples for new features
- Keep documentation clear and concise

## Questions?

Feel free to open an issue for any questions about contributing!

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
