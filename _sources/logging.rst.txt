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

   .. py:attribute:: created_at
      :type: int

      Timestamp when the log entry was created.

.. py:class:: WorkflowRun

   Contains information about a specific workflow run.

   .. py:attribute:: id
      :type: str

      Unique identifier for the workflow run.

   .. py:attribute:: status
      :type: str

      Current status of the workflow run.

   .. py:attribute:: elapsed_time
      :type: float

      Time taken to execute the workflow.

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

.. py:class:: WorkflowNodeExecutions

   Container for a list of node executions.

   .. py:attribute:: data
      :type: List[WorkflowNodeExecution]

      List of node executions. 