# dify-user-client

A Python utility library for interacting with Dify as if you were using the UI. Perform any action available through the user interface.

## Installation

```bash
pip install dify-user-client
```

## Quick Start

```python
from dify_user_client import DifyClient, Credentials

# Initialize credentials with username and password
credentials = Credentials(username="your_username", password="your_password")

# Create a client with base URL
client = DifyClient(base_url="https://api.dify.ai", credentials=credentials)

# Use the client to interact with Dify API
# Example: Get all applications
applications = client.apps
```

## Features

- **DifyClient**: A client for interacting with the Dify API
- **Credentials**: A class for managing API credentials
- **Comprehensive API Coverage**: Support for all major Dify API endpoints

## Documentation

For more detailed documentation, please visit [the documentation page](https://github.com/ivan-pikulin/dify_user_client).

## Development

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/ivan-pikulin/dify_user_client.git
   cd dify_user_client
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   # Using uv (recommended)
   uv venv
   uv pip install -e .
   
   # Using pip
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -e .
   ```

### Running Tests

```bash
# Install test dependencies
uv pip install -e ".[dev]"

# Run tests
pytest
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
