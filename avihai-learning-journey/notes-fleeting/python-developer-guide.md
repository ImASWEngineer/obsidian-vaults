# Developer Guide

## Table of Contents
- [Project Structure](#project-structure)
- [Development Setup](#development-setup)
- [Code Organization](#code-organization)
- [Adding New Features](#adding-new-features)
- [Testing](#testing)
- [Debugging](#debugging)
- [Performance Optimization](#performance-optimization)
- [Code Style](#code-style)
- [Documentation](#documentation)
- [Release Process](#release-process)

## Project Structure

```
pdf-to-markdown/
├── docs/                   # Documentation files
├── src/                    # Source code
│   ├── __init__.py
│   ├── cli.py              # Command-line interface
│   ├── config.py           # Configuration management
│   ├── converter.py        # Main conversion logic
│   ├── image_processor.py  # Image processing utilities
│   ├── text_extractor.py   # Text extraction logic
│   └── utils.py            # Helper functions
├── tests/                  # Test files
│   ├── __init__.py
│   ├── test_converter.py
│   ├── test_image_processor.py
│   └── test_text_extractor.py
├── .env.example           # Example environment variables
├── config.ini            # Configuration file
├── requirements.txt       # Dependencies
└── setup.py              # Package configuration
```

## Development Setup

1. **Fork and clone** the repository:
   ```bash
   git clone https://github.com/yourusername/pdf-to-markdown.git
   cd pdf-to-markdown
   ```

2. **Set up a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```

3. **Install development dependencies**:
   ```bash
   pip install -r requirements-dev.txt
   ```

4. **Install the package in development mode**:
   ```bash
   pip install -e .
   ```

5. **Set up pre-commit hooks**:
   ```bash
   pre-commit install
   ```

## Code Organization

The code is organized into the following modules:

### 1. CLI Module (`src/cli.py`)
- Handles command-line argument parsing
- Manages the conversion workflow
- Implements error handling and user feedback

### 2. Configuration (`src/config.py`)
- Loads and validates configuration
- Manages environment variables
- Handles default values and overrides

### 3. Converter (`src/converter.py`)
- Main conversion logic
- Coordinates between different components
- Manages the conversion pipeline

### 4. Image Processing (`src/image_processor.py`)
- Image extraction and processing
- OCR integration
- Diagram detection and conversion

### 5. Text Extraction (`src/text_extractor.py`)
- Text extraction from PDF
- Layout analysis
- Text cleaning and normalization

## Adding New Features

1. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Write tests** for your feature
3. **Implement the feature** following the code style
4. **Update documentation**
5. **Run tests** and ensure they pass
6. **Submit a pull request**

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run a specific test file
pytest tests/test_converter.py

# Run tests with coverage report
pytest --cov=src --cov-report=term-missing
```

### Writing Tests

- Place test files in the `tests/` directory
- Follow the naming convention `test_*.py`
- Use descriptive test function names
- Include docstrings explaining test cases

Example test:

```python
def test_pdf_conversion():
    """Test PDF to Markdown conversion with a sample file."""
    # Setup
    input_file = "tests/data/sample.pdf"
    output_file = "tests/output/sample.md"
    
    # Execute
    result = convert_pdf_to_markdown(input_file, output_file)
    
    # Verify
    assert result.success
    assert os.path.exists(output_file)
    with open(output_file) as f:
        content = f.read()
        assert "Sample Document" in content
```

## Debugging

### Logging

The application uses Python's `logging` module. Set the log level to `DEBUG` for detailed output:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Debug Mode

Run the script with `--debug` flag for additional debug information:

```bash
python -m src.cli --debug input.pdf output.md
```

### Using pdb

Insert breakpoints in the code:

```python
import pdb; pdb.set_trace()
```

## Performance Optimization

### Profiling

Use cProfile to identify performance bottlenecks:

```bash
python -m cProfile -o profile.cprof -m src.cli input.pdf output.md
snakeviz profile.cprof  # Visualize the profile
```

### Memory Profiling

Install `memory_profiler` and use the `@profile` decorator:

```python
from memory_profiler import profile

@profile
def process_pdf(input_file):
    # Your code here
    pass
```

## Code Style

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Use type hints
- Document public APIs with docstrings
- Keep functions small and focused
- Write meaningful variable and function names

### Linting

```bash
# Run linters
flake8 src/
mypy src/
black --check src/
```

### Auto-formatting

```bash
# Auto-format code
black src/

# Sort imports
isort src/
```

## Documentation

### Docstrings

Follow the Google style:

```python
def process_image(image_path: str, options: dict = None) -> Image:
    """Process an image file.

    Args:
        image_path: Path to the image file
        options: Optional processing options

    Returns:
        Processed image object

    Raises:
        FileNotFoundError: If the image file doesn't exist
        ValueError: If the image format is not supported
    """
    pass
```

### Building Documentation

```bash
# Install documentation dependencies
pip install -r docs/requirements.txt

# Build the documentation
cd docs
make html
```

## Release Process

1. **Update version** in `src/__init__.py`
2. **Update CHANGELOG.md**
3. **Create a release tag**:
   ```bash
   git tag -a v1.0.0 -m "Release v1.0.0"
   git push origin v1.0.0
   ```
4. **Build and publish** to PyPI:
   ```bash
   python -m build
   python -m twine upload dist/*
   ```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

Please ensure your code:
- Follows the existing style
- Includes tests
- Updates documentation as needed
- Has clear commit messages
