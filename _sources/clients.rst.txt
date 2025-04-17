Clients
=======

This section describes the client classes available in the Dify client library.

Basic Usage
-----------

Here are some common operations with the Dify client:

.. code-block:: python

   from dify_user_client import DifyClient, Credentials, AppType

   # Initialize client
   credentials = Credentials(username="your-email", password="your-password")
   client = DifyClient("https://your-dify-instance", credentials)

   # Create a new application
   new_app = client.create_app(
       name="My App",
       mode=AppType.chat,
       description="A chat application",
       icon_type="emoji",
       icon="🤖"
   )
   print(f"Created app with ID: {new_app.id}")

   # Get an existing application
   existing_app = client.get_app("your-app-id")
   print(f"Retrieved app: {existing_app.info['name']}")

   # List all applications
   all_apps = client.apps
   for app in all_apps:
       print(f"App: {app.info['name']} (ID: {app.id})")

   # Delete an application
   client.delete_app("app-to-delete-id")

Base Client
-----------

.. py:class:: DifyBaseClient

   Base client class providing core functionality.

   .. py:method:: __init__(base_url: str, credentials: Credentials)
      
      Initialize a new client.

      :param base_url: Base URL of the Dify API
      :param credentials: Authentication credentials

   .. py:method:: _login()
      
      Authenticate with the Dify API.

   .. py:method:: _send_user_request(method: str, url: str, **kwargs)
      
      Send an authenticated request to the API.

      :param method: HTTP method
      :param url: API endpoint URL
      :param kwargs: Additional request parameters

User Client
-----------

.. py:class:: DifyUserClient

   Client for user-facing operations.

   .. py:method:: update_timezone(timezone: str = "Europe/Moscow")
      
      Update user timezone setting.

   .. py:method:: update_system_model(model_settings: list[dict])
      
      Update system model settings.

   .. py:property:: apps() -> list[App]
      
      Get all available applications.

   .. py:method:: get_app(app_id: str) -> App
      
      Get a specific application by ID.

   .. py:property:: tool_providers() -> list[ToolProvider]
      
      Get all available tool providers.

   .. py:method:: get_tool_provider(provider_id: str) -> ToolProvider
      
      Get a specific tool provider by ID.

   .. py:property:: tools() -> list[Tool]
      
      Get all available tools.

   .. py:method:: get_tool(name: str) -> Tool
      
      Get a specific tool by name.

   .. py:property:: model_providers() -> list[ModelProvider]
      
      Get all available model providers.

   .. py:method:: get_model_provider(provider_id: str) -> ModelProvider
      
      Get a specific model provider by ID.

   .. py:method:: create_app(name: str, mode: AppType, description: str = "", icon_type: Literal["emoji", "image"] = "emoji", icon: str = "🤖", icon_background: str = "#FFEAD5") -> App
      
      Create a new application.

   .. py:method:: create_app_from_yaml(yaml_content: str) -> App
      
      Create a new application from YAML configuration.

   .. py:method:: delete_app(app_id: str)
      
      Delete an application.

Combined Client
--------------

.. py:class:: DifyClient

   Combined client providing access to both user and knowledge operations.

   .. py:method:: __init__(base_url: str, credentials: Credentials)
      
      Initialize a new combined client.

      :param base_url: Base URL of the Dify API
      :param credentials: Authentication credentials
      :ivar knowledge: Instance of :class:`DifyKnowledgeClient` for knowledge operations

Data Models
----------

.. py:class:: Credentials

   Authentication credentials.

   .. py:attribute:: username: str
      
      Username or email

   .. py:attribute:: password: str
      
      Password 