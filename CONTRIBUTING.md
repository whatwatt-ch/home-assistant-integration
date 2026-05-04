# Contributing to whatwatt

Thanks for your interest in contributing!

## Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/whatwatt-ch/home-assistant-integration.git
   cd home-assistant-integration
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -e ".[test]"
   ```

3. Run the test suite:
   ```bash
   pytest
   ```

## Running E2E Tests

E2E tests require Docker:

```bash
docker compose -f e2e/docker-compose.yml up -d
cd e2e
pip install -r requirements.txt
python -m pytest test_e2e.py -v
```

## Submitting Changes

1. Fork the repository and create a feature branch from `main`.
2. Make your changes and ensure all tests pass.
3. Submit a pull request with a clear description of what you changed and why.

## Reporting Bugs

Please use the [GitHub issue tracker](https://github.com/whatwatt-ch/home-assistant-integration/issues) and include:
- Home Assistant version
- whatwatt integration version
- Relevant log entries from Home Assistant
- Steps to reproduce the issue

## Code Style

- Follow the existing code conventions in the project.
- Use type hints where possible.
- Keep changes focused — one feature or fix per PR.
