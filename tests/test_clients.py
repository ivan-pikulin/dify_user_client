from dify_user_client import DifyClient

def test_client_models(client: DifyClient):
    assert isinstance(client, DifyClient)
