import time
from enum import Enum
from typing import Literal, Optional

import requests
from pydantic import BaseModel, Field

from .base import DifyBaseClient


class DatasetPermissionEnum(str, Enum):
    ONLY_ME = "only_me"
    ALL_TEAM = "all_team_members"
    PARTIAL_TEAM = "partial_members"


class DocumentIndexingStatuses(str, Enum):
    WAITING = "waiting"
    PARSING = "parsing"
    CLEANING = "cleaning"
    SPLITTING = "splitting"
    COMPLETED = "completed"
    INDEXING = "indexing"
    ERROR = "error"
    PAUSED = "paused"


class DocumentData(BaseModel):
    id: str
    dataset_id: str
    name: str
    content: str
    created_at: int
    updated_at: int
    indexing_status: DocumentIndexingStatuses
    word_count: int
    character_count: int
    segment_count: int
    metadata: dict = Field(default_factory=dict)


class KnowledgeToken(BaseModel):
    id: str
    type: Literal["dataset"]
    token: str
    last_used_at: Optional[int] = None
    created_at: int


class PreProcessingRule(BaseModel):
    id: Literal["remove_extra_spaces", "remove_urls_emails"]
    enabled: bool


class Segmentation(BaseModel):
    separator: Optional[str] = "###"
    max_tokens: Optional[int] = 500


class Rules(BaseModel):
    pre_processing_rules: list[PreProcessingRule] = []
    segmentation: Segmentation = Segmentation()


class ProcessRule(BaseModel):
    rules: Rules = Rules()
    mode: Literal["automatic", "custom"] = "automatic"


class KnowledgeSegmentSettings(BaseModel):
    name: Optional[str] = None
    indexing_technique: Literal["high_quality", "economy"] = "high_quality"
    process_rule: ProcessRule = ProcessRule()


class KnowledgeDocumentSegmentSettings(BaseModel):
    content: str = Field(...,
                         description="Text content / question content, required")
    answer: Optional[str] = Field(
        None, description="Answer content, if the mode of the knowledge is Q&A mode, pass the value (optional)")
    keywords: Optional[list[str]] = Field(
        None, description="Keywords (optional)")


class KnowledgeSegment:
    def __init__(self, id: str, client: 'DifyKnowledgeClient', dataset: 'KnowledgeDataset', document: 'KnowledgeDocument'):
        self.id = id
        self.client = client
        self.dataset = dataset
        self.document = document

    def update(self, settings: KnowledgeDocumentSegmentSettings):
        url = f"{self.client.base_url}/v1/datasets/{self.dataset.id}/documents/{self.document.id}/segments/{self.id}"
        self.client._send_api_request("POST", url, json=settings.model_dump())

    def delete(self):
        self.document.delete_segment(self.id)


class KnowledgeDocument:
    def __init__(self, id: str, client: 'DifyKnowledgeClient', dataset: 'KnowledgeDataset', batch_id: Optional[str] = None):
        self.id = id
        self.batch_id = batch_id
        self.client = client
        self.dataset = dataset

    def delete(self):
        self.dataset.delete_document(self.id)

    def create_segments(self, segments: list[KnowledgeDocumentSegmentSettings]) -> list[KnowledgeSegment]:
        url = f"{self.client.base_url}/v1/datasets/{self.dataset.id}/documents/{self.id}/segments"
        segments = [
            segment.model_dump() for segment in segments
        ]
        response = self.client._send_api_request(
            "POST", url, json={"segments": segments})
        return [
            KnowledgeSegment(
                id=segment['id'],
                client=self.client,
                dataset=self.dataset,
                document=self
            ) for segment in response["data"]
        ]

    @property
    def _segments_mapping(self) -> dict[str, KnowledgeSegment]:
        url = f"{self.client.base_url}/v1/datasets/{self.dataset.id}/documents/{self.id}/segments"
        response = self.client._send_api_request("GET", url)
        return {
            segment['id']: KnowledgeSegment(
                id=segment['id'],
                client=self.client,
                dataset=self.dataset,
                document=self
            ) for segment in response["data"]
        }

    @property
    def segments(self) -> list[KnowledgeSegment]:
        return list(self._segments_mapping.values())

    def get_segment(self, segment_id: str) -> KnowledgeSegment:
        try:
            return self._segments_mapping[segment_id]
        except KeyError:
            raise ValueError(f"Segment {segment_id} not found")

    def delete_segment(self, segment_id: str):
        url = f"{self.client.base_url}/v1/datasets/{self.dataset.id}/documents/{self.id}/segments/{segment_id}"
        self.client._send_api_request("DELETE", url)

    @property
    def indexing_status(self) -> DocumentIndexingStatuses:
        url = f"{self.client.base_url}/v1/datasets/{self.dataset.id}/documents/{self.batch_id}/indexing-status"
        response = self.client._send_api_request("GET", url)
        for document in response["data"]:
            if document["id"] == self.id:
                return document["indexing_status"]
        raise ValueError(f"Document {self.id} not found")

    def wait_for_indexing(self, timeout: int = 60) -> DocumentIndexingStatuses:
        start_time = time.time()
        while True:
            status = self.indexing_status
            if status in {"completed", "error"}:
                return status
            if time.time() - start_time > timeout:
                raise ValueError(f"Document {self.id} indexing failed")
            time.sleep(1)

    @property
    def data(self) -> DocumentData:
        """Fetch and return the document data."""
        url = f"{self.client.base_url}/console/api/datasets/{self.dataset.id}/documents/{self.id}"
        params = {"metadata": "without"}
        response = self.client._send_api_request("GET", url, params=params)
        return DocumentData.model_validate(response)


class KnowledgeDataset:
    def __init__(self, id: str, client: 'DifyKnowledgeClient', info: dict = None):

        self.id = id
        self.client = client
        self.info = info or {}

    @property
    def _documents_mapping(self) -> dict[str, KnowledgeDocument]:
        def fetch_documents(page):
            url = f"{self.client.base_url}/v1/datasets/{self.id}/documents?page={page}&limit=100"
            response = self.client._send_api_request("GET", url)
            return response['data'], response['has_more']

        documents = []
        page = 1
        while True:
            new_documents, has_more = fetch_documents(page)
            documents += new_documents
            page += 1
            if not has_more:
                break
        return {document['id']: KnowledgeDocument(id=document['id'], client=self.client, dataset=self) for document in documents}

    @property
    def documents(self) -> list[KnowledgeDocument]:
        return list(self._documents_mapping.values())

    def get_document(self, document_id: str) -> KnowledgeDocument:
        try:
            return self._documents_mapping[document_id]
        except KeyError:
            raise ValueError(f"Document {document_id} not found")

    def create_document_by_text(self, text: str, settings: KnowledgeSegmentSettings = None):
        if settings is None:
            settings = KnowledgeSegmentSettings()
        url = f"{self.client.base_url}/v1/datasets/{self.id}/document/create_by_text"
        data = settings.model_dump()
        data.update({"text": text})
        response = self.client._send_api_request("POST", url, json=data)
        return KnowledgeDocument(id=response['document']['id'], client=self.client, dataset=self, batch_id=response["batch"])

    def create_document_by_file(self, file_path: str, settings: KnowledgeSegmentSettings = None):
        if settings is None:
            settings = KnowledgeSegmentSettings()
        url = f"{self.client.base_url}/v1/datasets/{self.id}/document/create_by_file"
        response = self.client._send_api_request(
            "POST", url,
            data=settings.model_dump(),
            files={'file': open(file_path, 'rb')}
        )
        return KnowledgeDocument(id=response['id'], client=self.client, dataset=self, batch_id=response["batch"])

    def update_document_from_file(self, document_id: str, file_path: str, settings: KnowledgeSegmentSettings = None):
        if settings is None:
            settings = KnowledgeSegmentSettings()
        url = f"{self.client.base_url}/v1/datasets/{self.id}/documents/{document_id}/update-by-file"
        response = self.client._send_api_request(
            "POST", url,
            data=settings.model_dump(),
            files={'file': open(file_path, 'rb')}
        )
        return KnowledgeDocument(id=response['id'], client=self.client, dataset=self)

    def delete_document(self, document_id: str):
        url = f"{self.client.base_url}/v1/datasets/{self.id}/documents/{document_id}"
        self.client._send_api_request("DELETE", url)

    def delete(self):
        self.client.delete_dataset(self.id)


class DifyKnowledgeClient(DifyBaseClient):
    def _send_api_request(self, method: str, url: str, **kwargs):
        headers = kwargs.get("headers", {})
        headers["Authorization"] = f"Bearer {self.token.token}"

        response = requests.request(method, url, headers=headers, **kwargs)
        if response.status_code == 401:
            self._login()
            return self._send_user_request(method, url, headers=headers, **kwargs)
        if response.status_code not in (200, 201, 204):
            raise ValueError(
                f"Request failed: {response.status_code} - {response.text}")
        if method == "DELETE":
            return None
        else:
            return response.json()

    @property
    def _tokens_mapping(self) -> dict[str, KnowledgeToken]:
        """
        get a mapping of all available api keys for knowledge
        """
        url = f"{self.base_url}/console/api/datasets/api-keys"
        response = self._send_user_request("GET", url)
        return {data["id"]: KnowledgeToken(**data) for data in response["data"]}

    def get_token(self, token_id: str) -> KnowledgeToken:
        try:
            return self._tokens_mapping[token_id]
        except KeyError:
            raise ValueError(f"Token {token_id} not found")

    def create_token(self) -> KnowledgeToken:
        url = f"{self.base_url}/console/api/datasets/api-keys"
        response = self._send_user_request("POST", url)
        return KnowledgeToken(**response)

    def delete_token(self, token_id: str):
        url = f"{self.base_url}/console/api/datasets/api-keys/{token_id}"
        self._send_user_request("DELETE", url)

    @property
    def token(self) -> KnowledgeToken:
        tokens = list(self._tokens_mapping.values())
        if len(tokens) > 0:
            return tokens[0]
        else:
            return self.create_token()

    @property
    def _datasets_mapping(self) -> dict[str, KnowledgeDataset]:
        def fetch_datasets(page):
            url = f"{self.base_url}/v1/datasets?page={page}&limit=100"
            response = self._send_api_request("GET", url)
            datasets = [
                KnowledgeDataset(client=self, id=dataset['id'], info=dataset)
                for dataset in response['data']
            ]
            return datasets, response['has_more']

        datasets = []
        page = 1
        while True:
            new_datasets, has_more = fetch_datasets(page)
            datasets += new_datasets
            page += 1
            if not has_more:
                break
        return {dataset.id: dataset for dataset in datasets}

    @property
    def datasets(self) -> list[KnowledgeDataset]:
        return list(self._datasets_mapping.values())

    def get_dataset(self, dataset_id: str) -> KnowledgeDataset:
        try:
            return self._datasets_mapping[dataset_id]
        except KeyError:
            raise ValueError(f"Dataset {dataset_id} not found")

    def create_dataset(self, name: str, **kwargs) -> KnowledgeDataset:
        url = f"{self.base_url}/v1/datasets"
        response = self._send_api_request(
            "POST", url, json={"name": name, **kwargs})
        return KnowledgeDataset(client=self, id=response['id'], info=response)

    def delete_dataset(self, dataset_id: str):
        url = f"{self.base_url}/v1/datasets/{dataset_id}"
        self._send_api_request("DELETE", url)
