from dify_user_client import DifyClient
from dify_user_client.tools import Tool, ToolInfo

def test_tool_models(client: DifyClient):
    tools = client.tools
    assert isinstance(tools, list)
    assert len(tools) > 0

    for tool in tools:
        assert isinstance(tool, Tool)

    for tool in tools:
        assert isinstance(tool.info, ToolInfo)