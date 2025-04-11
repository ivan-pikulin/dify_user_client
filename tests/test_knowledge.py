import pytest

from dify_user_client import DifyClient
from dify_user_client.knowledge import (DifyKnowledgeClient, KnowledgeDocumentData, KnowledgeDataset,
                                  KnowledgeDocument,
                                  KnowledgeDocumentSegmentSettings,
                                  KnowledgeSegment, KnowledgeSegmentSettings,
                                  KnowledgeToken)


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
    try:
        dataset = knowledge.create_dataset(name="test_dataset")
        assert isinstance(dataset, KnowledgeDataset)
    finally:
        dataset.delete()

    with pytest.raises(ValueError, match=".*not found.*"):
        knowledge.get_dataset(dataset.id)


def test_create_delete_document(client: DifyClient):
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
        assert isinstance(document, KnowledgeDocument)
        document.delete()

        with pytest.raises(ValueError, match=".*not found.*"):
            dataset.get_document(document.id)
    finally:
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