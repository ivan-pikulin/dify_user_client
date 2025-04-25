Language Models
===============

This section describes the language model (LLM) functionality in the Dify client.

Model Provider Management
----------------------

.. py:class:: ModelProvider

   Represents a language model provider.

   .. py:method:: __init__(client: DifyBaseClient, id: str)
      
      Initialize a new model provider.

   .. py:property:: info() -> ModelProviderInfo
      
      Get provider information.

   .. py:method:: update_credentials(credentials: dict)
      
      Update provider credentials.

   .. py:method:: validate_credentials(credentials: dict)
      
      Validate provider credentials.

   .. py:method:: delete()
      
      Delete the provider.

Data Models
-----------

.. py:class:: SupportedModelType(str, Enum)

   Enumeration of supported model types.

   .. py:attribute:: text_embedding
      Text embedding models
   
   .. py:attribute:: speech2text
      Speech-to-text models
   
   .. py:attribute:: moderation
      Content moderation models
   
   .. py:attribute:: tts
      Text-to-speech models
   
   .. py:attribute:: llm
      Language models
   
   .. py:attribute:: rerank
      Reranking models

.. py:class:: ModelProviderInfo

   Information about a model provider.

   .. py:attribute:: provider: str
      Provider identifier

   .. py:attribute:: label: Optional[Union[dict, str]]
      Display label

   .. py:attribute:: description: Optional[Union[dict, str]]
      Provider description

   .. py:attribute:: icon_small: Optional[Union[dict, str]]
      Small icon URL

   .. py:attribute:: icon_large: Optional[Union[dict, str]]
      Large icon URL

   .. py:attribute:: background: Optional[str]
      Background color

   .. py:attribute:: help: Optional[ModelProviderHelp]
      Help information

   .. py:attribute:: supported_model_types: list[SupportedModelType]
      List of supported model types

   .. py:attribute:: configurate_methods: Optional[list[str]]
      Available configuration methods

   .. py:attribute:: preferred_provider_type: Optional[Literal["predefined", "custom"]]
      Preferred provider type

.. py:class:: ModelProviderHelp

   Help information for a model provider.

   .. py:attribute:: title: Union[dict, str]
      Help title

   .. py:attribute:: url: Union[dict, str]
      Help documentation URL 