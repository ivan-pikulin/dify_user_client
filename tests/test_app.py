from abc import ABC

import pytest
import yaml

from dify_user_client import DifyClient
from dify_user_client.apps import (AdvancedChatApp, AgentApp, App, AppType,
                                   ChatApp, CompletionApp, WorkflowApp)
from dify_user_client.models.logs import (AgentConversation,
                                          PaginatedAgentLogs,
                                          PaginatedWorkflowLogs,
                                          WorkflowLogEntry)


def test_app_models(client: DifyClient):
    apps = client.apps
    assert isinstance(apps, list)

    for app in apps:
        assert isinstance(app, App)


class BaseTestApp(ABC):
    mode = None
    app_class = None

    def test_create_delete_app(self, client: DifyClient):
        app = client.create_app(name=f"test-{self.mode}-app", mode=self.mode)
        assert isinstance(app, self.app_class)
        app = client.get_app(app_id=app.id)
        assert isinstance(app, self.app_class)
        app.delete()

        with pytest.raises(ValueError, match=".*not found.*"):
            client.get_app(app_id=app.id)

    def test_export_yaml(self, client: DifyClient):
        app = client.create_app(name=f"test-{self.mode}-app", mode=self.mode)
        try:
            yaml_content = app.export_yaml()
            parsed_yaml = yaml.safe_load(yaml_content)
            assert isinstance(parsed_yaml, dict)

        finally:
            app.delete()

    def test_create_from_yaml(self, client: DifyClient):
        agent_app = client.create_app(
            name=f"test-{self.mode}-app", mode=self.mode)
        try:

            yaml_content = agent_app.export_yaml()
            new_agent_app = client.create_app_from_yaml(yaml_content)
            assert isinstance(new_agent_app, self.app_class)
            new_agent_app = client.get_app(new_agent_app.id)
            assert isinstance(new_agent_app, self.app_class)
            new_agent_app.delete()

        finally:
            agent_app.delete()


class TestAgentApp(BaseTestApp):
    mode = AppType.agent
    app_class = AgentApp

    def test_import_yaml(self, client: DifyClient):
        agent_app = client.create_app(
            name=f"test-{self.mode}-app",
            mode=self.mode)
        try:
            agent_app.import_yaml(agent_app.export_yaml())
            assert isinstance(agent_app, self.app_class)

        finally:
            agent_app.delete()

    def test_get_logs(self, client: DifyClient):
        app = client.create_app(name=f"test-{self.mode}-app", mode=self.mode)
        try:
            logs = app.get_logs(page=1, limit=10)
            assert isinstance(logs, PaginatedAgentLogs)
            assert isinstance(logs.page, int)
            assert isinstance(logs.limit, int)
            assert isinstance(logs.total, int)
            assert isinstance(logs.has_more, bool)
            assert isinstance(logs.data, list)
            
            if logs.data:
                assert isinstance(logs.data[0], AgentConversation)
        finally:
            app.delete()

    def test_iter_logs(self, client: DifyClient):
        app = client.create_app(name=f"test-{self.mode}-app", mode=self.mode)
        try:
            logs_count = 0
            for log in app.iter_logs(limit=10):
                assert isinstance(log, AgentConversation)
                logs_count += 1
                if logs_count >= 15:  # Test at least a few pages
                    break
        finally:
            app.delete()


class TestChatApp(BaseTestApp):
    mode = AppType.chat
    app_class = ChatApp


class TestCompletionApp(BaseTestApp):
    mode = AppType.completion
    app_class = CompletionApp


class TestWorkflowApp(BaseTestApp):
    mode = AppType.workflow
    app_class = WorkflowApp

    def test_import_yaml(self, client: DifyClient):
        workflow_app = client.create_app(
            name=f"test-{self.mode}-app",
            mode=self.mode)
        try:
            workflow_app.import_yaml(workflow_app.export_yaml())
            assert isinstance(workflow_app, self.app_class)
        finally:
            workflow_app.delete()

    def test_get_logs(self, client: DifyClient):
        app = client.create_app(name=f"test-{self.mode}-app", mode=self.mode)
        try:
            logs = app.get_logs(page=1, limit=10)
            assert isinstance(logs, PaginatedWorkflowLogs)
            assert isinstance(logs.page, int)
            assert isinstance(logs.limit, int)
            assert isinstance(logs.total, int)
            assert isinstance(logs.has_more, bool)
            assert isinstance(logs.data, list)
            
            if logs.data:
                assert isinstance(logs.data[0], WorkflowLogEntry)
        finally:
            app.delete()

    def test_iter_logs(self, client: DifyClient):
        app = client.create_app(name=f"test-{self.mode}-app", mode=self.mode)
        try:
            logs_count = 0
            for log in app.iter_logs(limit=10):
                assert isinstance(log, WorkflowLogEntry)
                logs_count += 1
                if logs_count >= 15:  # Test at least a few pages
                    break
        finally:
            app.delete()


class TestAdvancedChatApp(BaseTestApp):
    mode = AppType.advanced_chat
    app_class = AdvancedChatApp
