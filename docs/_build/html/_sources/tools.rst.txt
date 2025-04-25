Tools
=====

This section describes the tools functionality in the Dify client.

Tool Providers
--------------

.. py:class:: ToolProvider

   Base class for tool providers.

   .. py:classmethod:: create(client: DifyBaseClient, id: str, type: Literal["workflow", "builtin"]) -> ToolProvider
      
      Factory method to create a tool provider.

   .. py:property:: tool_info
      
      Get tool provider information.

.. py:class:: WorkflowToolProvider

   Provider for workflow-based tools.

   .. py:property:: info() -> WorkflowToolProviderInfo
      
      Get workflow tool provider information.

   .. py:property:: tools() -> list[WorkflowTool]
      
      Get list of workflow tools.

.. py:class:: BuiltinToolProvider

   Provider for built-in tools.

   .. py:property:: tools() -> list[BuiltinTool]
      
      Get list of built-in tools.

   .. py:property:: tools_info() -> dict[str, ToolInfo]
      
      Get information about all tools.

   .. py:method:: update_credentials(credentials: dict)
      
      Update provider credentials.

Tools
-----

.. py:class:: Tool

   Base class for tools.

   .. py:classmethod:: create(client: DifyBaseClient, provider: ToolProvider, name: str, mode: Literal["workflow", "builtin"]) -> Tool
      
      Factory method to create a tool.

   .. py:property:: info() -> ToolInfo
      
      Get tool information.

.. py:class:: WorkflowTool

   Workflow-based tool implementation.

   .. py:property:: workflow_app_id() -> str
      
      Get associated workflow app ID.

   .. py:property:: info() -> ToolInfo
      
      Get tool information.

.. py:class:: BuiltinTool

   Built-in tool implementation.

   .. py:property:: info() -> ToolInfo
      
      Get tool information.

Data Models
-----------

.. py:class:: ToolInfo

   Information about a tool.

   .. py:attribute:: author: str
      Tool author

   .. py:attribute:: name: str
      Tool name

   .. py:attribute:: label: Union[dict, str]
      Display label

   .. py:attribute:: description: Union[dict, str]
      Tool description

   .. py:attribute:: parameters: list[ToolParameter]
      Tool parameters

   .. py:attribute:: labels: list[str]
      Tool labels

.. py:class:: ToolParameter

   Tool parameter configuration.

   .. py:attribute:: name: str
      Parameter name

   .. py:attribute:: label: Union[dict, str]
      Display label

   .. py:attribute:: human_description: Optional[Union[dict, str]]
      Human-readable description

   .. py:attribute:: placeholder: Optional[Union[dict, str]]
      Placeholder text

   .. py:attribute:: type: Literal["string", "number", "boolean", "select", "file", "files", "secret-input"]
      Parameter type

   .. py:attribute:: form: Literal["llm", "form"]
      Form type

   .. py:attribute:: llm_description: Optional[str]
      Description for LLM

   .. py:attribute:: required: bool
      Whether parameter is required

.. py:class:: WorkflowToolProviderInfo

   Information about a workflow tool provider.

   .. py:attribute:: name: str
      Provider name

   .. py:attribute:: label: str
      Display label

   .. py:attribute:: workflow_tool_id: Optional[str]
      Tool ID

   .. py:attribute:: workflow_app_id: str
      Associated workflow app ID

   .. py:attribute:: description: str
      Provider description

   .. py:attribute:: parameters: list[WorkflowToolParameter]
      Tool parameters 