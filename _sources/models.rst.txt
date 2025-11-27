Data Models
===========

This section describes the data models used in the Dify client.

App Token
---------

.. py:class:: AppToken

   Represents an API token for an application.

   .. py:attribute:: id: str
      
      Unique identifier for the token

   .. py:attribute:: type: Literal["app"]
      
      Token type, always "app"

   .. py:attribute:: token: str
      
      The actual token string

   .. py:attribute:: last_used_at: Optional[int]
      
      Timestamp of last usage

   .. py:attribute:: created_at: int
      
      Timestamp of creation

Workflow Models
-------------

.. py:class:: WorkflowDraft

   Represents a workflow configuration draft.

   .. py:attribute:: graph: Optional[Graph]
      
      The workflow graph structure

   .. py:attribute:: features: dict
      
      Feature configuration

   .. py:attribute:: environment_variables: list
      
      Environment variables used in the workflow

   .. py:attribute:: conversation_variables: list
      
      Conversation variables used in the workflow

Graph Models
-----------

.. py:class:: Graph

   Represents the complete workflow graph structure.

   .. py:attribute:: nodes: list[GraphNode]
      
      List of nodes in the graph

   .. py:attribute:: edges: list[GraphEdge]
      
      List of edges connecting the nodes

   .. py:attribute:: viewport: Viewport
      
      View configuration for the graph

.. py:class:: GraphNode

   Represents a node in the workflow graph.

   .. py:attribute:: id: str
      
      Unique identifier for the node

   .. py:attribute:: type: str
      
      Node type

   .. py:attribute:: data: dict
      
      Node configuration data

   .. py:attribute:: position: dict
      
      Node position in the graph

   .. py:attribute:: targetPosition: str
      
      Position of target connection point

   .. py:attribute:: sourcePosition: str
      
      Position of source connection point

   .. py:attribute:: positionAbsolute: dict
      
      Absolute position in the graph

   .. py:attribute:: width: int
      
      Node width

   .. py:attribute:: height: int
      
      Node height

.. py:class:: GraphEdge

   Represents an edge connecting two nodes in the workflow graph.

   .. py:attribute:: id: str
      
      Unique identifier for the edge

   .. py:attribute:: type: str
      
      Edge type

   .. py:attribute:: source: str
      
      Source node ID

   .. py:attribute:: sourceHandle: str
      
      Source connection point

   .. py:attribute:: target: str
      
      Target node ID

   .. py:attribute:: targetHandle: str
      
      Target connection point

   .. py:attribute:: data: GraphEdgeData
      
      Edge configuration data

   .. py:attribute:: zIndex: int
      
      Z-index for rendering

.. py:class:: GraphEdgeData

   Configuration data for graph edges.

   .. py:attribute:: sourceType: GraphNodeDataTypes
      
      Type of the source node

   .. py:attribute:: targetType: GraphNodeDataTypes
      
      Type of the target node

   .. py:attribute:: isInIteration: bool
      
      Whether the edge is part of an iteration

.. py:class:: GraphNodeData

   Configuration data for graph nodes.

   .. py:attribute:: type: GraphNodeDataTypes
      
      Node type (start, end, or llm)

   .. py:attribute:: title: str
      
      Node title

   .. py:attribute:: description: str
      
      Node description

   .. py:attribute:: variables: list
      
      List of variables used by the node

.. py:class:: Viewport

   Graph view configuration.

   .. py:attribute:: x: Optional[int]
      
      X coordinate of the viewport (default: 0)

   .. py:attribute:: y: Optional[int]
      
      Y coordinate of the viewport (default: 0)

   .. py:attribute:: zoom: Optional[int]
      
      Zoom level (default: 1)

Base Models
-----------

.. py:class:: BaseModel

   Base model with common functionality for all data models.

   .. py:attribute:: id
      :type: Optional[str]
      
      Unique identifier

   .. py:attribute:: created_at
      :type: Optional[int]
      
      Creation timestamp

   .. py:attribute:: updated_at
      :type: Optional[int]
      
      Last update timestamp

   .. py:method:: to_dict() -> dict
      
      Convert the model to a dictionary.

      :return: Dictionary representation of the model

   .. py:property:: created_datetime -> Optional[datetime]
      
      Get creation timestamp as datetime object.

      :return: Datetime object or None

   .. py:property:: updated_datetime -> Optional[datetime]
      
      Get update timestamp as datetime object.

      :return: Datetime object or None

Pagination Models
-----------------

.. py:class:: PaginatedResponse

   Generic paginated response model.

   .. py:attribute:: page
      :type: int
      
      Current page number

   .. py:attribute:: limit
      :type: int
      
      Number of items per page

   .. py:attribute:: total
      :type: int
      
      Total number of items

   .. py:attribute:: has_more
      :type: bool
      
      Whether there are more pages

   .. py:attribute:: data
      :type: List[T]
      
      List of items in the current page

   .. py:method:: __iter__() -> Iterator[T]
      
      Make the response iterable over data items.

      :return: Iterator over data items

   .. py:method:: __len__() -> int
      
      Get the number of items in the current page.

      :return: Number of items

Logging Models
--------------

.. py:class:: AgentConversation

   Represents a single agent or chat conversation.

   .. py:attribute:: id
      :type: str
      
      Unique identifier for the conversation

   .. py:attribute:: status
      :type: str
      
      Current status of the conversation

   .. py:attribute:: from_source
      :type: str
      
      Source from which the conversation originated

   .. py:attribute:: from_end_user_id
      :type: Optional[str]
      
      ID of the end user who started the conversation

   .. py:attribute:: from_end_user_session_id
      :type: Optional[str]
      
      Session ID of the end user

   .. py:attribute:: from_account_id
      :type: Optional[str]
      
      Account ID of the creator

   .. py:attribute:: from_account_name
      :type: Optional[str]
      
      Name of the account creator

   .. py:attribute:: name
      :type: str
      
      Name of the conversation

   .. py:attribute:: summary
      :type: str
      
      Summary of the conversation

   .. py:attribute:: read_at
      :type: Optional[int]
      
      Timestamp when the conversation was last read

   .. py:attribute:: created_at
      :type: int
      
      Timestamp when the conversation was created

   .. py:attribute:: updated_at
      :type: int
      
      Timestamp when the conversation was last updated

   .. py:attribute:: annotated
      :type: bool
      
      Whether the conversation has been annotated

   .. py:attribute:: agent_model_config
      :type: Dict
      
      Model configuration for the agent (aliased as "model_config" in API)

   .. py:attribute:: message_count
      :type: int
      
      Number of messages in the conversation

   .. py:attribute:: user_feedback_stats
      :type: Dict
      
      Statistics about user feedback

   .. py:attribute:: admin_feedback_stats
      :type: Dict
      
      Statistics about admin feedback

   .. py:attribute:: status_count
      :type: Dict
      
      Count of different statuses

.. py:class:: ChatMessage

   Represents a single chat message in a conversation.

   .. py:attribute:: id
      :type: str
      
      Unique identifier for the message

   .. py:attribute:: conversation_id
      :type: str
      
      ID of the conversation this message belongs to

   .. py:attribute:: inputs
      :type: Optional[Dict[str, Any]]
      
      Input parameters provided with the message

   .. py:attribute:: query
      :type: Optional[str]
      
      The user's query or question

   .. py:attribute:: answer
      :type: Optional[str]
      
      The assistant's answer

   .. py:attribute:: message
      :type: Optional[Dict[str, Any]]
      
      Full message object with additional metadata

   .. py:attribute:: feedback
      :type: Optional[Dict[str, Any]]
      
      User feedback on the message

   .. py:attribute:: created_at
      :type: int
      
      Timestamp when the message was created

   .. py:attribute:: created_by_role
      :type: Optional[str]
      
      Role of the user who created the message

   .. py:attribute:: created_by_account
      :type: Optional[Dict[str, Any]]
      
      Account information of the creator

   .. py:attribute:: created_by_end_user
      :type: Optional[Dict[str, Any]]
      
      End user information

   .. py:attribute:: from_source
      :type: Optional[str]
      
      Source from which the message originated

   .. py:attribute:: from_end_user_id
      :type: Optional[str]
      
      ID of the end user

   .. py:attribute:: from_end_user_session_id
      :type: Optional[str]
      
      Session ID of the end user

   .. py:attribute:: from_account_id
      :type: Optional[str]
      
      Account ID of the creator

   .. py:attribute:: from_account_name
      :type: Optional[str]
      
      Name of the account creator

.. py:class:: PaginatedChatMessages

   Paginated response containing chat messages.

   Inherits from :class:`PaginatedResponse` with :class:`ChatMessage` as the item type.

   .. py:attribute:: data
      :type: List[ChatMessage]
      
      List of chat messages in the current page

   .. py:attribute:: page
      :type: int
      
      Current page number

   .. py:attribute:: limit
      :type: int
      
      Number of items per page

   .. py:attribute:: total
      :type: int
      
      Total number of items

   .. py:attribute:: has_more
      :type: bool
      
      Whether there are more pages available

.. py:class:: PaginatedAgentLogs

   Paginated response containing agent conversation logs.

   Inherits from :class:`PaginatedResponse` with :class:`AgentConversation` as the item type.

   .. py:attribute:: data
      :type: List[AgentConversation]
      
      List of conversations in the current page

   .. py:attribute:: page
      :type: int
      
      Current page number

   .. py:attribute:: limit
      :type: int
      
      Number of items per page

   .. py:attribute:: total
      :type: int
      
      Total number of items

   .. py:attribute:: has_more
      :type: bool
      
      Whether there are more pages available

.. py:class:: PaginatedWorkflowLogs

   Paginated response containing workflow execution logs.

   Inherits from :class:`PaginatedResponse` with :class:`WorkflowLogEntry` as the item type.

   .. py:attribute:: data
      :type: List[WorkflowLogEntry]
      
      List of workflow log entries in the current page

   .. py:attribute:: page
      :type: int
      
      Current page number

   .. py:attribute:: limit
      :type: int
      
      Number of items per page

   .. py:attribute:: total
      :type: int
      
      Total number of items

   .. py:attribute:: has_more
      :type: bool
      
      Whether there are more pages available

Workflow Execution Models
-------------------------

.. py:class:: WorkflowNodeExecutionMetadata

   Metadata about workflow node execution.

   .. py:attribute:: parallel_id
      :type: Optional[str]
      
      ID for parallel execution

   .. py:attribute:: parallel_start_node_id
      :type: Optional[str]
      
      ID of the starting node in parallel execution

   .. py:attribute:: tool_info
      :type: Optional[Dict[str, Any]]
      
      Information about tools used

   .. py:attribute:: total_tokens
      :type: Optional[int]
      
      Total tokens used

   .. py:attribute:: total_price
      :type: Optional[str]
      
      Total price of execution

   .. py:attribute:: currency
      :type: Optional[str]
      
      Currency for the price

.. py:class:: WorkflowNodeExecutions

   Container for a list of node executions.

   .. py:attribute:: data
      :type: List[WorkflowNodeExecution]
      
      List of node executions 