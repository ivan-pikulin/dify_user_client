.. dify_user_client documentation master file, created by
   sphinx-quickstart on Thu Apr 17 11:06:22 2025.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

dify_user_client
================

The Dify User Client is a Python library for interacting with the Dify API. It provides a comprehensive set of tools for managing applications, knowledge bases, language models, and more.

Installation
------------

Install using UV (recommended):

.. code-block:: bash

   uv pip install dify-user-client

Quick Start
-----------

To use the Dify client, first create an instance with your credentials:

.. code-block:: python

   from dify_user_client import DifyClient, Credentials

   credentials = Credentials(username="your-email", password="your-password")
   client = DifyClient("https://your-dify-instance", credentials)

   # Create a new chat application
   app = client.create_app("My Chat App", mode="chat")

   # Get application info
   app_info = app.info
   print(f"App ID: {app.id}")
   print(f"App Type: {app.type}")

   # Get an existing application by ID
   existing_app = client.get_app("your-app-id")
   print(f"Retrieved app: {existing_app.info['name']}")

Key Features
------------

- **Multiple App Types**: Support for chat, completion, workflow, and agent applications
- **Knowledge Base Management**: Create and manage knowledge bases
- **LLM Integration**: Work with various language models
- **Token Management**: Secure API token handling
- **Workflow Tools**: Advanced workflow creation and management
- **Type Safety**: Full type hints support with Pydantic models

Contents
--------

.. toctree::
   :maxdepth: 3
   :caption: Core Documentation

   ./clients
   ./apps
   ./knowledge
   ./tools
   ./logging

.. toctree::
   :maxdepth: 2
   :caption: Advanced Features

   ./models
   ./llms

.. toctree::
   :maxdepth: 2
   :caption: Development

   contributing
   changelog

