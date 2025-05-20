from typing import Optional, Dict, List, Any, Literal
from enum import Enum

from .base import BaseModel

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

class RetrievalMethod(str, Enum):
    SEMANTIC_SEARCH = "semantic_search"
    FULL_TEXT_SEARCH = "full_text_search"
    HYBRID_SEARCH = "hybrid_search"

class KnowledgeToken(BaseModel):
    type: Literal["dataset"]
    token: str
    last_used_at: Optional[int] = None

class PreProcessingRule(BaseModel):
    id: Literal["remove_extra_spaces", "remove_urls_emails"]
    enabled: bool

class Segmentation(BaseModel):
    separator: Optional[str] = "###"
    max_tokens: Optional[int] = 1000

class Rules(BaseModel):
    pre_processing_rules: List[PreProcessingRule]
    segmentation: Segmentation

class ProcessRule(BaseModel):
    mode: Literal["automatic", "custom"]
    rules: Rules

class VectorSetting(BaseModel):
    vector_weight: float = 0.8

class KeywordSetting(BaseModel):
    keyword_weight: float = 0.2

class RetrievalWeights(BaseModel):
    vector_setting: VectorSetting
    keyword_setting: KeywordSetting

class RetrievalModelDict(BaseModel):
    search_method: RetrievalMethod
    weights: Optional[RetrievalWeights] = None

class KnowledgeDatasetSettings(BaseModel):
    name: str
    description: Optional[str] = None
    provider: str = "vendor"
    permission: DatasetPermissionEnum = DatasetPermissionEnum.ONLY_ME
    data_source_type: Optional[str] = None
    indexing_technique: Literal["high_quality", "economy"] = "high_quality"
    app_count: int = 0
    document_count: int = 0
    word_count: int = 0
    created_by: Optional[str] = None
    updated_by: Optional[str] = None
    embedding_model: Optional[str] = None
    embedding_model_provider: Optional[str] = None
    embedding_available: Optional[bool] = None
    retrieval_model_dict: Optional[RetrievalModelDict] = None
    tags: List[str] = []
    external_knowledge_info: Optional[Dict] = None
    external_retrieval_model: Optional[Dict] = None

class KnowledgeDocumentData(BaseModel):
    id: str
    name: str
    content: Optional[str] = None
    doc_type: Optional[str] = None
    doc_status: Optional[str] = None
    doc_metadata: Optional[Dict] = None
    doc_form: Optional[str] = None
    doc_language: Optional[str] = None
    indexing_status: Optional[DocumentIndexingStatuses] = None
    process_rule: Optional[ProcessRule] = None
    created_by: Optional[str] = None
    created_at: Optional[int] = None
    updated_by: Optional[str] = None
    updated_at: Optional[int] = None
    tokens: Optional[int] = None
    segments_count: Optional[int] = None
    enabled: Optional[bool] = True
    disabled_at: Optional[int] = None
    disabled_by: Optional[str] = None
    archived: Optional[bool] = False
    display_status: Optional[str] = None
    error: Optional[str] = None

class KnowledgeDocument(BaseModel):
    id: str
    dataset_id: str
    name: str
    content: str
    indexing_status: DocumentIndexingStatuses
    process_rule: ProcessRule
    created_at: int
    updated_at: Optional[int] = None

class KnowledgeDocumentSegmentSettings(BaseModel):
    content: str
    answer: Optional[str] = None
    keywords: Optional[List[str]] = None

class KnowledgeSegmentSettings(BaseModel):
    name: str
    indexing_technique: Literal["high_quality", "economy"] = "high_quality"
    process_rule: ProcessRule

class RerankingModel(BaseModel):
    reranking_provider_name: Optional[str]
    reranking_model_name: Optional[str]

class WeightSettings(BaseModel):
    weight_type: Optional[str] = "customized"
    vector_setting: VectorSetting
    keyword_setting: KeywordSetting

class ExternalKnowledgeInfo(BaseModel):
    external_knowledge_id: Optional[str] = None
    external_knowledge_api_id: Optional[str] = None
    external_knowledge_api_name: Optional[str] = None
    external_knowledge_api_endpoint: Optional[str] = None

class ExternalRetrievalModel(BaseModel):
    top_k: int
    score_threshold: Optional[float] = None
    score_threshold_enabled: Optional[bool] = False 