Dataset Settings
================

The Knowledge Dataset Settings API allows you to manage dataset configurations including retrieval methods, reranking settings, and permissions.

Basic Usage
----------

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
--------------------

Retrieval Methods
~~~~~~~~~~~~~~~

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
~~~~~~~~~~

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
----------------

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