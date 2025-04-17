Contributing
============

We welcome contributions to the `dify_user_client` library! This guide will help you get started with development.

Development Setup
-----------------

1. Clone the repository:

   .. code-block:: bash

      git clone https://github.com/ivan-pikulin/dify_user_client.git
      cd dify_user_client

2. Set up the development environment:

   .. code-block:: bash

      uv venv
      uv pip install -e ".[dev]"

3. Install development dependencies:

   .. code-block:: bash

      uv pip install -r requirements-dev.txt

Code Style
----------

We follow these Python coding conventions:

- Use type hints for all function signatures
- Follow PEP 8 style guide
- Use descriptive variable names with auxiliary verbs
- Implement proper error handling with early returns
- Write comprehensive tests for new features

Testing
-------

Run the test suite:

.. code-block:: bash

   uv run pytest

Documentation
-------------

Build the documentation locally:

.. code-block:: bash

   cd docs
   uv run make html

The built documentation will be in ``docs/build/html``. 