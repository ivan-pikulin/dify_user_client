Logging and Chat History
=====================

This section describes the logging and chat history functionality in the Dify client.

Chat Session
-----------

.. py:class:: Chat

   Represents a chat conversation session. Used for tracking and retrieving message history.

   .. py:method:: __init__(client: DifyBaseClient, app: App, id: str, info: dict = None)
      
      Initialize a new chat session.

      :param client: The Dify client instance
      :param app: The parent application instance
      :param id: Unique identifier for the chat session
      :param info: Optional additional information about the chat session

   .. py:property:: messages(max_pages: int = 10) -> list
      
      Retrieves chat messages for the conversation, with pagination support.
      Returns a list of message dictionaries.

      :param max_pages: Maximum number of pages to retrieve (default: 10)
      :return: List of message dictionaries containing conversation history 