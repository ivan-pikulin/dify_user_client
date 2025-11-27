Logging and Chat History
========================

The Dify client provides comprehensive logging functionality for both workflow and chat applications.

Quick Examples
--------------

.. code-block:: python

    # Get workflow logs
    workflow_app = client.get_app(app_id="your-workflow-app-id")
    
    # Get paginated logs
    logs = workflow_app.get_logs(page=1, limit=10)
    for entry in logs.data:
        print(f"Workflow run {entry.workflow_run.id}: {entry.workflow_run.status}")
    
    # Iterate through all logs
    for entry in workflow_app.iter_logs(limit=10):
        print(f"Log entry {entry.id} created at {entry.created_at}")
    
    # Get workflow node executions
    workflow_run_id = logs.data[0].workflow_run.id
    executions = workflow_app.get_node_executions(workflow_run_id)
    for node in executions.data:
        print(f"Node {node.title} ({node.node_type}): {node.status}")
        if node.error:
            print(f"Error: {node.error}")
    
    # Get agent/chat conversation logs
    agent_app = client.get_app(app_id="your-agent-app-id")
    conversations = agent_app.get_logs(page=1, limit=10)
    for conversation in conversations.data:
        print(f"Conversation {conversation.id}: {conversation.name}")
    
    # Get messages for a conversation
    conversation_id = conversations.data[0].id
    messages = agent_app.get_messages(conversation_id=conversation_id, limit=10)
    for message in messages.data:
        print(f"Message: {message.query}")
        if message.answer:
            print(f"Answer: {message.answer}")

Chat Session
------------

.. py:class:: Chat

   Represents a chat conversation session. Used for tracking and retrieving message history.

   .. py:method:: __init__(client: DifyBaseClient, app: App, id: str, info: dict = None)
      
      Initialize a new chat session.

      :param client: The Dify client instance
      :param app: The parent application instance
      :param id: Unique identifier for the chat session
      :param info: Optional additional information about the chat session

   .. py:property:: messages(max_pages: int = 10) -> list
      
      Retrieves chat messages for the conversation, with pagination support.
      Returns a list of message dictionaries.

      :param max_pages: Maximum number of pages to retrieve (default: 10)
      :return: List of message dictionaries containing conversation history 

Workflow Logging
----------------

.. py:class:: WorkflowLogEntry

   Represents a single workflow execution log entry.

   .. py:attribute:: id
      :type: str

      Unique identifier for the log entry.

   .. py:attribute:: workflow_run
      :type: WorkflowRun

      Details about the workflow run.

   .. py:attribute:: created_from
      :type: str

      Source from which the workflow was created.

   .. py:attribute:: created_by_role
      :type: str

      Role of the user who created the workflow run.

   .. py:attribute:: created_by_account
      :type: Optional[Dict]

      Account information of the creator.

   .. py:attribute:: created_by_end_user
      :type: Dict

      End user information.

   .. py:attribute:: created_at
      :type: int

      Timestamp when the log entry was created.

.. py:class:: WorkflowRun

   Contains information about a specific workflow run.

   .. py:attribute:: id
      :type: str

      Unique identifier for the workflow run.

   .. py:attribute:: version
      :type: str

      Version of the workflow.

   .. py:attribute:: status
      :type: str

      Current status of the workflow run.

   .. py:attribute:: error
      :type: Optional[str]

      Error message if the workflow run failed.

   .. py:attribute:: elapsed_time
      :type: float

      Time taken to execute the workflow.

   .. py:attribute:: total_tokens
      :type: int

      Total number of tokens used.

   .. py:attribute:: total_steps
      :type: int

      Total number of steps executed.

   .. py:attribute:: created_at
      :type: int

      Timestamp when the workflow run was created.

   .. py:attribute:: finished_at
      :type: int

      Timestamp when the workflow run finished.

   .. py:attribute:: exceptions_count
      :type: int

      Number of exceptions encountered during execution.

Workflow Node Executions
------------------------

.. py:class:: WorkflowNodeExecution

   Represents the execution of a single node in a workflow.

   .. py:attribute:: id
      :type: str

      Unique identifier for the node execution.

   .. py:attribute:: node_type
      :type: str

      Type of the workflow node.

   .. py:attribute:: title
      :type: str

      Title of the node.

   .. py:attribute:: status
      :type: str

      Execution status of the node.

   .. py:attribute:: error
      :type: Optional[str]

      Error message if the node execution failed.

   .. py:attribute:: elapsed_time
      :type: float

      Time taken to execute the node.

   .. py:attribute:: inputs
      :type: Optional[Dict[str, Any]]

      Input parameters provided to the node.

   .. py:attribute:: outputs
      :type: Optional[Dict[str, Any]]

      Output values produced by the node.

   .. py:attribute:: process_data
      :type: Optional[Dict[str, Any]]

      Process data during node execution.

   .. py:attribute:: index
      :type: int

      Index of the node execution.

   .. py:attribute:: predecessor_node_id
      :type: Optional[str]

      ID of the predecessor node.

   .. py:attribute:: node_id
      :type: str

      ID of the node being executed.

   .. py:attribute:: execution_metadata
      :type: Optional[WorkflowNodeExecutionMetadata]

      Metadata about the node execution.

   .. py:attribute:: extras
      :type: Dict[str, Any]

      Additional extra data.

   .. py:attribute:: created_at
      :type: int

      Timestamp when the node execution was created.

   .. py:attribute:: created_by_role
      :type: str

      Role of the user who triggered the execution.

   .. py:attribute:: created_by_account
      :type: Optional[Dict[str, Any]]

      Account information of the creator.

   .. py:attribute:: created_by_end_user
      :type: Dict[str, Any]

      End user information.

   .. py:attribute:: finished_at
      :type: int

      Timestamp when the node execution finished.

.. py:class:: WorkflowNodeExecutionMetadata

   Metadata about workflow node execution.

   .. py:attribute:: parallel_id
      :type: Optional[str]

      ID for parallel execution.

   .. py:attribute:: parallel_start_node_id
      :type: Optional[str]

      ID of the starting node in parallel execution.

   .. py:attribute:: tool_info
      :type: Optional[Dict[str, Any]]

      Information about tools used.

   .. py:attribute:: total_tokens
      :type: Optional[int]

      Total tokens used.

   .. py:attribute:: total_price
      :type: Optional[str]

      Total price of execution.

   .. py:attribute:: currency
      :type: Optional[str]

      Currency for the price.

.. py:class:: WorkflowNodeExecutions

   Container for a list of node executions.

   .. py:attribute:: data
      :type: List[WorkflowNodeExecution]

      List of node executions.

Agent and Chat Logging
-----------------------

.. py:class:: AgentConversation

   Represents a single agent or chat conversation.

   .. py:attribute:: id
      :type: str

      Unique identifier for the conversation.

   .. py:attribute:: status
      :type: str

      Current status of the conversation.

   .. py:attribute:: from_source
      :type: str

      Source from which the conversation originated.

   .. py:attribute:: from_end_user_id
      :type: Optional[str]

      ID of the end user who started the conversation.

   .. py:attribute:: from_end_user_session_id
      :type: Optional[str]

      Session ID of the end user.

   .. py:attribute:: from_account_id
      :type: Optional[str]

      Account ID of the creator.

   .. py:attribute:: from_account_name
      :type: Optional[str]

      Name of the account creator.

   .. py:attribute:: name
      :type: str

      Name of the conversation.

   .. py:attribute:: summary
      :type: str

      Summary of the conversation.

   .. py:attribute:: read_at
      :type: Optional[int]

      Timestamp when the conversation was last read.

   .. py:attribute:: created_at
      :type: int

      Timestamp when the conversation was created.

   .. py:attribute:: updated_at
      :type: int

      Timestamp when the conversation was last updated.

   .. py:attribute:: annotated
      :type: bool

      Whether the conversation has been annotated.

   .. py:attribute:: agent_model_config
      :type: Dict

      Model configuration for the agent (aliased as "model_config" in API).

   .. py:attribute:: message_count
      :type: int

      Number of messages in the conversation.

   .. py:attribute:: user_feedback_stats
      :type: Dict

      Statistics about user feedback.

   .. py:attribute:: admin_feedback_stats
      :type: Dict

      Statistics about admin feedback.

   .. py:attribute:: status_count
      :type: Dict

      Count of different statuses.

Chat Messages
------------

.. py:class:: ChatMessage

   Represents a single chat message in a conversation.

   .. py:attribute:: id
      :type: str

      Unique identifier for the message.

   .. py:attribute:: conversation_id
      :type: str

      ID of the conversation this message belongs to.

   .. py:attribute:: inputs
      :type: Optional[Dict[str, Any]]

      Input parameters provided with the message.

   .. py:attribute:: query
      :type: Optional[str]

      The user's query or question.

   .. py:attribute:: answer
      :type: Optional[str]

      The assistant's answer.

   .. py:attribute:: message
      :type: Optional[Dict[str, Any]]

      Full message object with additional metadata.

   .. py:attribute:: feedback
      :type: Optional[Dict[str, Any]]

      User feedback on the message.

   .. py:attribute:: created_at
      :type: int

      Timestamp when the message was created.

   .. py:attribute:: created_by_role
      :type: Optional[str]

      Role of the user who created the message.

   .. py:attribute:: created_by_account
      :type: Optional[Dict[str, Any]]

      Account information of the creator.

   .. py:attribute:: created_by_end_user
      :type: Optional[Dict[str, Any]]

      End user information.

   .. py:attribute:: from_source
      :type: Optional[str]

      Source from which the message originated.

   .. py:attribute:: from_end_user_id
      :type: Optional[str]

      ID of the end user.

   .. py:attribute:: from_end_user_session_id
      :type: Optional[str]

      Session ID of the end user.

   .. py:attribute:: from_account_id
      :type: Optional[str]

      Account ID of the creator.

   .. py:attribute:: from_account_name
      :type: Optional[str]

      Name of the account creator.

.. py:class:: PaginatedChatMessages

   Paginated response containing chat messages.

   .. py:attribute:: data
      :type: List[ChatMessage]

      List of chat messages in the current page.

   .. py:attribute:: page
      :type: int

      Current page number.

   .. py:attribute:: limit
      :type: int

      Number of items per page.

   .. py:attribute:: total
      :type: int

      Total number of items.

   .. py:attribute:: has_more
      :type: bool

      Whether there are more pages available.

.. py:class:: PaginatedAgentLogs

   Paginated response containing agent conversation logs.

   .. py:attribute:: data
      :type: List[AgentConversation]

      List of conversations in the current page.

   .. py:attribute:: page
      :type: int

      Current page number.

   .. py:attribute:: limit
      :type: int

      Number of items per page.

   .. py:attribute:: total
      :type: int

      Total number of items.

   .. py:attribute:: has_more
      :type: bool

      Whether there are more pages available. 