import pytest
import time

from dify_user_client import DifyClient
from dify_user_client.knowledge import (
    DifyKnowledgeClient, KnowledgeDataset, KnowledgeSegment,
    KnowledgeDocument
)
from dify_user_client.models import (
    DatasetPermissionEnum, KnowledgeDatasetSettings, KnowledgeDocumentData,
    KnowledgeSegmentSettings, KnowledgeToken, RetrievalMethod,
    KnowledgeDocumentSegmentSettings
)

def get_unique_name(prefix: str = "test") -> str:
    return f"{prefix}_{int(time.time())}"

def test_knowledge_models(client: DifyClient):
    knowledge = client.knowledge
    assert isinstance(knowledge, DifyKnowledgeClient)
    assert isinstance(knowledge.datasets, list)

    for dataset in knowledge.datasets:
        assert isinstance(dataset, KnowledgeDataset)

    assert isinstance(knowledge.token, KnowledgeToken)

    for token in knowledge._tokens_mapping.values():
        assert isinstance(token, KnowledgeToken)


def test_create_delete_token(client: DifyClient):
    knowledge = client.knowledge
    token = knowledge.create_token()
    assert isinstance(token, KnowledgeToken)

    knowledge.delete_token(token.id)

    with pytest.raises(ValueError, match=".*not found.*"):
        knowledge.get_token(token.id)


def test_create_delete_dataset(client: DifyClient):
    knowledge = client.knowledge
    dataset = None
    try:
        dataset = knowledge.create_dataset(name=get_unique_name("test_dataset"))
        assert isinstance(dataset, KnowledgeDataset)
    finally:
        if dataset:
            dataset.delete()

    with pytest.raises(ValueError, match=".*not found.*"):
        knowledge.get_dataset(dataset.id)


def test_create_delete_document(client: DifyClient):
    knowledge = client.knowledge
    dataset = None
    try:
        dataset = knowledge.create_dataset(name=get_unique_name("test_dataset"))
        document = dataset.create_document_by_text(
            text="test_content",
            settings=KnowledgeSegmentSettings(
                **{
                    "name": get_unique_name("test_document"),
                    "indexing_technique": "high_quality",
                    "process_rule": {
                        "mode": "automatic",
                        "rules": {
                            "pre_processing_rules": [
                                {
                                    "id": "remove_extra_spaces",
                                    "enabled": True
                                }
                            ],
                            "segmentation": {
                                "separator": "###",
                                "max_tokens": 1000
                            }
                        }
                    }
                }
            )
        )
        assert isinstance(document, KnowledgeDocument)
        document.delete()

        with pytest.raises(ValueError, match=".*not found.*"):
            dataset.get_document(document.id)
    finally:
        if dataset:
            dataset.delete()

    with pytest.raises(ValueError, match=".*not found.*"):
        knowledge.get_dataset(dataset.id)


def test_create_delete_segment(client: DifyClient):
    knowledge = client.knowledge
    try:
        dataset = knowledge.create_dataset(name="test_dataset")
        document = dataset.create_document_by_text(
            text="test_content",
            settings=KnowledgeSegmentSettings(
                **{
                    "name": "test",
                    "indexing_technique": "high_quality",
                    "process_rule": {
                        "mode": "automatic",
                        "rules": {
                            "pre_processing_rules": [
                                {
                                    "id": "remove_extra_spaces",
                                    "enabled": True
                                }
                            ],
                            "segmentation": {
                                "separator": "###",
                                "max_tokens": 1000
                            }
                        }
                    }
                }
            )
        )
        document.wait_for_indexing(timeout=10)
        segments = document.create_segments(
            segments=[
                KnowledgeDocumentSegmentSettings(
                    content="test_segment",
                    answer="test_answer",
                    keywords=["test_keyword"]
                )
            ]
        )
        assert isinstance(segments, list)

        for segment in segments:
            assert isinstance(segment, KnowledgeSegment)

        for segment in segments:
            segment.delete()

        for segment in segments:
            with pytest.raises(ValueError, match=".*not found.*"):
                document.get_segment(segment.id)

        document.delete()

        with pytest.raises(ValueError, match=".*not found.*"):
            dataset.get_document(document.id)
    finally:
        dataset.delete()

    with pytest.raises(ValueError, match=".*not found.*"):
        knowledge.get_dataset(dataset.id)

def test_get_document_data(client: DifyClient):
    knowledge = client.knowledge
    try:
        dataset = knowledge.create_dataset(name="test_dataset")
        document = dataset.create_document_by_text(
            text="test_content",
            settings=KnowledgeSegmentSettings(
                **{
                    "name": "test_document",
                    "indexing_technique": "high_quality",
                    "process_rule": {
                        "mode": "automatic",
                        "rules": {
                            "pre_processing_rules": [
                                {
                                    "id": "remove_extra_spaces",
                                    "enabled": True
                                }
                            ],
                            "segmentation": {
                                "separator": "###",
                                "max_tokens": 1000
                            }
                        }
                    }
                }
            )
        )
        document.wait_for_indexing(timeout=10)
        data = document.data
        assert isinstance(data, KnowledgeDocumentData)
        document.delete()

        with pytest.raises(ValueError, match=".*not found.*"):
            dataset.get_document(document.id)
    finally:
        dataset.delete()

    with pytest.raises(ValueError, match=".*not found.*"):
        knowledge.get_dataset(dataset.id)


def test_dataset_settings(client: DifyClient):
    knowledge = client.knowledge
    try:
        # Create a dataset with initial settings
        dataset = knowledge.create_dataset(
            name="test_dataset_settings",
            description="Initial description",
            permission=DatasetPermissionEnum.ONLY_ME,
            indexing_technique="high_quality"
        )
        
        # Get and verify settings
        settings = dataset.settings
        assert isinstance(settings, KnowledgeDatasetSettings)
        assert settings.name == "test_dataset_settings"
        assert settings.description == "Initial description"
        assert settings.permission == DatasetPermissionEnum.ONLY_ME
        assert settings.indexing_technique == "high_quality"
        assert settings.retrieval_model_dict.search_method == RetrievalMethod.SEMANTIC_SEARCH
        
        # Update settings
        dataset.update_settings(
            name="updated_dataset_settings",
            description="Updated description",
            permission=DatasetPermissionEnum.ALL_TEAM,
            retrieval_model={
                "search_method": RetrievalMethod.HYBRID_SEARCH,
                "weights": {
                    "vector_setting": {
                        "vector_weight": 0.8
                    },
                    "keyword_setting": {
                        "keyword_weight": 0.2
                    }
                }
            }
        )
        
        # Get and verify updated settings
        updated_settings = dataset.settings
        assert updated_settings.name == "updated_dataset_settings"
        assert updated_settings.description == "Updated description"
        assert updated_settings.permission == DatasetPermissionEnum.ALL_TEAM
        assert updated_settings.retrieval_model_dict.search_method == RetrievalMethod.HYBRID_SEARCH
        assert updated_settings.retrieval_model_dict.weights.vector_setting.vector_weight == 0.8
        assert updated_settings.retrieval_model_dict.weights.keyword_setting.keyword_weight == 0.2
        
    finally:
        dataset.delete()
