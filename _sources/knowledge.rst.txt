Knowledge
=========

This section describes the knowledge base functionality available in the Dify client library.

Dataset Management
----------------

.. py:class:: KnowledgeDataset

   Represents a knowledge dataset that can contain multiple documents.

   .. py:method:: __init__(id: str, client: DifyKnowledgeClient, info: dict = None)
      
      Initialize a new dataset.

   .. py:property:: documents() -> list[KnowledgeDocument]
      
      Returns all documents in the dataset.

   .. py:method:: get_document(document_id: str) -> KnowledgeDocument
      
      Retrieve a specific document by ID.

   .. py:method:: create_document_by_text(text: str, settings: KnowledgeSegmentSettings = None) -> KnowledgeDocument
      
      Create a new document from text content.

   .. py:method:: create_document_by_file(file_path: str, settings: KnowledgeSegmentSettings = None) -> KnowledgeDocument
      
      Create a new document from a file.

   .. py:method:: update_document_from_file(document_id: str, file_path: str, settings: KnowledgeSegmentSettings = None) -> KnowledgeDocument
      
      Update an existing document with new file content.

   .. py:method:: delete_document(document_id: str)
      
      Delete a document from the dataset.

   .. py:method:: delete()
      
      Delete the entire dataset.

Document
--------

.. py:class:: KnowledgeDocument

   Represents a document within a knowledge dataset.

   .. py:method:: __init__(id: str, client: DifyKnowledgeClient, dataset: KnowledgeDataset, batch_id: Optional[str] = None)
      
      Initialize a new document.

   .. py:property:: segments() -> list[KnowledgeSegment]
      
      Returns all segments in the document.

   .. py:method:: create_segments(segments: list[KnowledgeDocumentSegmentSettings]) -> list[KnowledgeSegment]
      
      Create multiple segments in the document.

   .. py:method:: get_segment(segment_id: str) -> KnowledgeSegment
      
      Retrieve a specific segment by ID.

   .. py:method:: delete_segment(segment_id: str)
      
      Delete a segment from the document.

   .. py:property:: indexing_status() -> DocumentIndexingStatuses
      
      Get the current indexing status of the document.

   .. py:method:: wait_for_indexing(timeout: int = 60) -> DocumentIndexingStatuses
      
      Wait for document indexing to complete.

   .. py:property:: data() -> KnowledgeDocumentData
      
      Get detailed document data.

   .. py:method:: delete()
      
      Delete the document.

Segment
-------

.. py:class:: KnowledgeSegment

   Represents a segment within a document.

   .. py:method:: __init__(id: str, client: DifyKnowledgeClient, dataset: KnowledgeDataset, document: KnowledgeDocument)
      
      Initialize a new segment.

   .. py:method:: update(settings: KnowledgeDocumentSegmentSettings)
      
      Update segment settings.

   .. py:method:: delete()
      
      Delete the segment.

Data Models
-----------

.. py:class:: DatasetPermissionEnum(str, Enum)

   Enumeration of dataset permission levels.

   .. py:attribute:: ONLY_ME
      
      Only the creator can access

   .. py:attribute:: ALL_TEAM
      
      All team members can access

   .. py:attribute:: PARTIAL_TEAM
      
      Selected team members can access

.. py:class:: DocumentIndexingStatuses(str, Enum)

   Enumeration of document indexing states.

   .. py:attribute:: WAITING
   .. py:attribute:: PARSING
   .. py:attribute:: CLEANING
   .. py:attribute:: SPLITTING
   .. py:attribute:: COMPLETED
   .. py:attribute:: INDEXING
   .. py:attribute:: ERROR
   .. py:attribute:: PAUSED

.. py:class:: KnowledgeToken

   Represents an API token for knowledge operations.

   .. py:attribute:: id: str
   .. py:attribute:: type: Literal["dataset"]
   .. py:attribute:: token: str
   .. py:attribute:: last_used_at: Optional[int]
   .. py:attribute:: created_at: int

.. py:class:: KnowledgeSegmentSettings

   Settings for knowledge segment processing.

   .. py:attribute:: name: Optional[str]
   .. py:attribute:: indexing_technique: Literal["high_quality", "economy"]
   .. py:attribute:: process_rule: ProcessRule

.. py:class:: KnowledgeDocumentSegmentSettings

   Settings for document segments.

   .. py:attribute:: content: str
      Text content / question content

   .. py:attribute:: answer: Optional[str]
      Answer content for Q&A mode

   .. py:attribute:: keywords: Optional[list[str]]
      Optional keywords

.. py:class:: KnowledgeDocumentData

   Detailed document information.

   .. py:attribute:: id: str
   .. py:attribute:: name: str
   .. py:attribute:: data_source_type: str
   .. py:attribute:: indexing_status: DocumentIndexingStatuses
   .. py:attribute:: tokens: int
   .. py:attribute:: segment_count: int
   .. py:attribute:: average_segment_length: int
   .. py:attribute:: hit_count: int
   .. py:attribute:: display_status: Literal["queuing", "paused", "indexing", "error", "available", "disabled", "archived"]

Hit
--- 

Dataset Settings
----------------

The Knowledge Dataset Settings API allows you to manage dataset configurations including retrieval methods, reranking settings, and permissions.

Basic Usage
~~~~~~~~~~~

.. code-block:: python

    from dify_user_client import DifyClient
    from dify_user_client.knowledge import DatasetPermissionEnum, RetrievalMethod

    # Initialize client
    client = DifyClient("YOUR_API_KEY")
    
    # Get dataset
    dataset = client.knowledge.get_dataset("dataset_id")
    
    # Get current settings
    settings = dataset.settings
    
    # Update settings
    dataset.update_settings(
        name="Updated Dataset",
        description="New description",
        permission=DatasetPermissionEnum.ALL_TEAM,
        retrieval_model={
            "search_method": RetrievalMethod.HYBRID_SEARCH,
            "weights": {
                "vector_setting": {"vector_weight": 0.7},
                "keyword_setting": {"keyword_weight": 0.3}
            }
        }
    )

Settings Configuration
~~~~~~~~~~~~~~~~~~~~~~

Retrieval Methods
'''''''''''''''''

The API supports three retrieval methods:

- ``SEMANTIC_SEARCH``: Uses embeddings for semantic similarity search
- ``FULL_TEXT_SEARCH``: Uses keyword-based search
- ``HYBRID_SEARCH``: Combines both semantic and keyword search

.. code-block:: python

    # Configure semantic search
    dataset.update_settings(
        retrieval_model={
            "search_method": RetrievalMethod.SEMANTIC_SEARCH,
            "weights": {
                "vector_setting": {"vector_weight": 1.0},
                "keyword_setting": {"keyword_weight": 0.0}
            }
        }
    )

Permissions
'''''''''''

Dataset access can be controlled with the following permission levels:

- ``ONLY_ME``: Only the creator can access
- ``ALL_TEAM``: All team members can access
- ``PARTIAL_TEAM``: Selected team members can access

.. code-block:: python

    # Update permissions
    dataset.update_settings(
        permission=DatasetPermissionEnum.ALL_TEAM
    )

Settings Properties
~~~~~~~~~~~~~~~~~~~

The dataset settings object includes the following properties:

- ``id``: Dataset identifier
- ``name``: Dataset name
- ``description``: Optional dataset description
- ``permission``: Access permission level
- ``indexing_technique``: "high_quality" or "economy"
- ``retrieval_model_dict``: Retrieval configuration
  - ``search_method``: Search method to use
  - ``weights``: Weight configuration for hybrid search
  - ``top_k``: Number of results to return
  - ``score_threshold``: Minimum score threshold
- ``embedding_model``: Name of the embedding model
- ``embedding_model_provider``: Provider of the embedding model 