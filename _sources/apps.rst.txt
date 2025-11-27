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

   from dify_user_client import DifyClient, Credentials, AppType

   # Create client
   client = DifyClient("https://your-dify-instance", Credentials(...))

   # Create app using factory method
   app = App.create(client=client, id="app-id", mode=AppType.chat)
   
   # Or create via client
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
   
   # Access chats
   chats = app.chats                  # Get all chat conversations
   for chat in chats:
       print(f"Chat ID: {chat.id}")
       messages = chat.messages       # Get messages for this chat

.. py:classmethod:: App.create(client: DifyBaseClient, id: str, mode: AppType) -> App

   Factory method to create an App instance of the appropriate type.

   :param client: The Dify client instance
   :param id: Application ID
   :param mode: Application type (AppType)
   :return: App instance (WorkflowApp, AgentApp, ChatApp, CompletionApp, or AdvancedChatApp)

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

.. py:class:: Chat

   Represents a chat conversation session.

   .. py:attribute:: id
      :type: str
      
      Unique identifier for the chat session.

   .. py:attribute:: app
      :type: App
      
      The parent application instance.

   .. py:attribute:: client
      :type: DifyBaseClient
      
      The Dify client instance.

   .. py:attribute:: info
      :type: dict
      
      Additional information about the chat session.

   .. py:property:: messages(max_pages: int = 10) -> list
      
      Retrieves chat messages for the conversation, with pagination support.
      Returns a list of message dictionaries.

      :param max_pages: Maximum number of pages to retrieve (default: 10)
      :return: List of message dictionaries containing conversation history

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
   workflow_app.publish_as_tool(config)  # Publish as tool, returns workflow tool id
   
   # Get tool provider info
   tool_info = workflow_app.tool_info
   
   # Get workflow logs
   logs = workflow_app.get_logs(page=1, limit=10)
   for entry in logs.data:
       print(f"Workflow run: {entry.workflow_run.id}, Status: {entry.workflow_run.status}")
   
   # Iterate through all logs
   for entry in workflow_app.iter_logs(limit=10):
       print(f"Log entry {entry.id} created at {entry.created_at}")
   
   # Get node executions for a workflow run
   workflow_run_id = logs.data[0].workflow_run.id
   executions = workflow_app.get_node_executions(workflow_run_id)
   for node in executions.data:
       print(f"Node {node.title} ({node.node_type}): {node.status}")
       if node.error:
           print(f"Error: {node.error}")

.. py:method:: WorkflowApp.get_logs(page: int = 1, limit: int = 10) -> PaginatedWorkflowLogs

   Get paginated workflow execution logs.

   :param page: Page number (default: 1)
   :param limit: Number of items per page (default: 10)
   :return: PaginatedWorkflowLogs containing workflow log entries

.. py:method:: WorkflowApp.iter_logs(limit: int = 10) -> Generator[WorkflowLogEntry, None, None]

   Iterate through all workflow logs with automatic pagination.

   :param limit: Number of items per page (default: 10)
   :return: Generator yielding WorkflowLogEntry objects

.. py:method:: WorkflowApp.get_node_executions(workflow_run_id: str) -> WorkflowNodeExecutions

   Get node executions for a specific workflow run.

   :param workflow_run_id: ID of the workflow run
   :return: WorkflowNodeExecutions containing list of node executions

.. py:property:: WorkflowApp.tool_info -> WorkflowToolProviderInfo

   Get workflow tool provider information.

   :return: WorkflowToolProviderInfo object

Agent Applications
------------------

``AgentApp`` is specialized for agent-based interactions:

.. code-block:: python

   agent_app = client.create_app("My Agent", mode=AppType.agent)
   
   # Import configuration
   agent_app.import_yaml(yaml_content)
   
   # Get conversation logs
   logs = agent_app.get_logs(page=1, limit=10)
   for conversation in logs.data:
       print(f"Conversation {conversation.id}: {conversation.name}")
       print(f"Status: {conversation.status}, Messages: {conversation.message_count}")
   
   # Iterate through all conversation logs
   for conversation in agent_app.iter_logs(limit=10):
       print(f"Conversation: {conversation.name}")
   
   # Get messages for a specific conversation
   conversation_id = logs.data[0].id
   messages = agent_app.get_messages(conversation_id=conversation_id, limit=10, page=1)
   for message in messages.data:
       print(f"Message {message.id}: {message.query}")
       if message.answer:
           print(f"Answer: {message.answer}")

.. py:method:: AgentApp.get_logs(page: int = 1, limit: int = 10) -> PaginatedAgentLogs

   Get paginated agent conversation logs.

   :param page: Page number (default: 1)
   :param limit: Number of items per page (default: 10)
   :return: PaginatedAgentLogs containing agent conversation entries

.. py:method:: AgentApp.iter_logs(limit: int = 10) -> Generator[AgentConversation, None, None]

   Iterate through all agent conversation logs with automatic pagination.

   :param limit: Number of items per page (default: 10)
   :return: Generator yielding AgentConversation objects

.. py:method:: AgentApp.get_messages(conversation_id: str, limit: int = 10, page: int = 1) -> PaginatedChatMessages

   Get chat messages for a specific conversation.

   :param conversation_id: The ID of the conversation to get messages from
   :param limit: Maximum number of messages to return (default: 10)
   :param page: Page number to retrieve (default: 1)
   :return: PaginatedChatMessages containing ChatMessage objects

Chat Applications
-----------------

``ChatApp`` provides chat-specific functionality:

.. code-block:: python

   chat_app = client.create_app("My Chat", mode=AppType.chat)
   
   # Get conversation logs
   logs = chat_app.get_logs(page=1, limit=10)
   for conversation in logs.data:
       print(f"Conversation {conversation.id}: {conversation.name}")
   
   # Iterate through all conversation logs
   for conversation in chat_app.iter_logs(limit=10):
       print(f"Conversation: {conversation.name}")

.. py:method:: ChatApp.get_logs(page: int = 1, limit: int = 10) -> PaginatedAgentLogs

   Get paginated chat conversation logs.

   :param page: Page number (default: 1)
   :param limit: Number of items per page (default: 10)
   :return: PaginatedAgentLogs containing conversation entries

.. py:method:: ChatApp.iter_logs(limit: int = 10) -> Generator[AgentConversation, None, None]

   Iterate through all chat conversation logs with automatic pagination.

   :param limit: Number of items per page (default: 10)
   :return: Generator yielding AgentConversation objects

Completion Applications
-----------------------

``CompletionApp`` is for completion-based applications:

.. code-block:: python

   completion_app = client.create_app("My Completion", mode=AppType.completion)
   
   # Use base App functionality
   app_info = completion_app.info
   completion_app.update_info({"name": "New Name"})

Advanced Chat Applications
--------------------------

``AdvancedChatApp`` combines features of both ``ChatApp`` and ``WorkflowApp``:

.. code-block:: python

   advanced_app = client.create_app("Advanced Chat", mode=AppType.advanced_chat)
   
   # Use both chat and workflow features
   chats = advanced_app.chats
   advanced_app.update_draft(draft)
   
   # Use chat logging
   logs = advanced_app.get_logs(page=1, limit=10)
   
   # Use workflow features
   workflow_logs = advanced_app.get_logs(page=1, limit=10)

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