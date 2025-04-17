Applications
============

The dify_user_client provides several application types to suit different needs.

App Types
---------

.. code-block:: python

   from dify_user_client import AppType

   # Available app types
   AppType.workflow       # For workflow-based applications
   AppType.chat          # For simple chat applications
   AppType.advanced_chat # For advanced chat with workflow features
   AppType.agent        # For agent-based applications
   AppType.completion   # For completion-based applications

Base App Class
--------------

The base ``App`` class provides common functionality for all application types:

.. code-block:: python

   from dify_user_client import DifyClient, Credentials

   # Create client
   client = DifyClient("https://your-dify-instance", Credentials(...))

   # Create app
   app = client.create_app("My App", mode=AppType.chat)

   # Common operations
   app_info = app.info                # Get app information
   app.update_info({"name": "New Name"})  # Update app information
   app.delete()                       # Delete the app
   
   # Token management
   token = app.token                  # Get or create default token
   all_tokens = app.tokens            # List all tokens
   new_token = app.create_token()     # Create new token

   # Export configuration
   yaml_config = app.export_yaml()    # Export app configuration as YAML

Chat Management
---------------

All app types support chat functionality:

.. code-block:: python

   # List all chats
   chats = app.chats

   # Access chat messages
   for chat in chats:
       messages = chat.messages  # Get chat messages
       print(f"Chat {chat.id}: {len(messages)} messages")

Workflow Applications
---------------------

``WorkflowApp`` provides additional features for workflow-based applications:

.. code-block:: python

   from dify_user_client import WorkflowDraft, Graph

   workflow_app = client.create_app("My Workflow", mode=AppType.workflow)

   # Update workflow draft
   draft = WorkflowDraft(
       graph=Graph(...),
       features={},
       environment_variables=[],
       conversation_variables=[]
   )
   workflow_app.update_draft(draft)

   # Get current draft
   current_draft = workflow_app.get_draft()

   # Import/Export
   workflow_app.import_yaml(yaml_content)
   
   # Publishing
   workflow_app.publish()  # Publish workflow
   workflow_app.publish_as_tool(config)  # Publish as tool

Agent Applications
------------------

``AgentApp`` is specialized for agent-based interactions:

.. code-block:: python

   agent_app = client.create_app("My Agent", mode=AppType.agent)
   
   # Import configuration
   agent_app.import_yaml(yaml_content)

Advanced Chat Applications
--------------------------

``AdvancedChatApp`` combines features of both ``ChatApp`` and ``WorkflowApp``:

.. code-block:: python

   advanced_app = client.create_app("Advanced Chat", mode=AppType.advanced_chat)
   
   # Use both chat and workflow features
   chats = advanced_app.chats
   advanced_app.update_draft(draft)

Type Safety
-----------

All models use Pydantic for type safety:

.. code-block:: python

   from dify_user_client.apps import WorkflowDraft, Graph, GraphNode, GraphEdge

   # Create type-safe models
   node = GraphNode(
       id="node1",
       type="start",
       data={"type": "start", "title": "Start", "description": "", "variables": []},
       position={"x": 0, "y": 0},
       targetPosition="left",
       sourcePosition="right",
       positionAbsolute={"x": 0, "y": 0},
       width=150,
       height=50
   )