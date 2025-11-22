"""Basic chat handler."""

import logging
import uuid
from abc import ABC, abstractmethod
from collections.abc import Iterator

from langchain_core.messages import HumanMessage
from langchain_core.vectorstores import VectorStoreRetriever
from langchain_openai import ChatOpenAI
from langgraph.graph import START, MessagesState, StateGraph
from langgraph.checkpoint.memory import MemorySaver

from oracle_server.error import ChatError
from oracle_server.vectorstore import ChromaVectorStore

_LOGGER = logging.getLogger()

# todo: move to config
DEFAULT_MODEL_TEMP = 0.7
DEFAULT_TOP_K = 5
DEFAULT_SQLITE_DIR = "./chromadb"
DEFAULT_VECTOR_COLLECTION = "babylon_vectors"
DEFAULT_CHAT_MEMORY_KEY = "chat_history"
DEFAULT_OPEN_API_KEY = "ollama"


# todo: add factory
# pylint: disable=too-many-instance-attributes
class ChatHandler(ABC):
    """Base Chat Handler which all implementations should inherit from."""

    def __init__(
        self,
        embedding_model: str,
        llm_model: str,
        model_url: str | None = None,
        thread_id: str | None = None,
    ):
        """
        Constructor.

        :param llm_model: Model identifier.
        """
        self._embedding_model = embedding_model
        self._llm_model = llm_model
        self._model_url = model_url
        # Set up hyper params.
        self._hyper_parameters = {
            "temperature": DEFAULT_MODEL_TEMP,
            "top_k": DEFAULT_TOP_K,
        }
        self._vector_store = ChromaVectorStore(
            model=self._embedding_model,
            sqlite_dir=DEFAULT_SQLITE_DIR,
            collection=DEFAULT_VECTOR_COLLECTION,
        )
        self._chatbot = self.retrieve_chatbot()
        self._vector_retriever = self._retrieve_vectors()
        self._thread_id = thread_id or str(uuid.uuid4())
        self._config = {"configurable": {"thread_id": self._thread_id}}
        try:
            _LOGGER.info("Compiling LangGraph workflow")
            self._workflow = self._create_workflow()
            self._app = self._workflow.compile(checkpointer=MemorySaver())
        except Exception as e:
            message = f"Error compiling workflow for thread {self._thread_id}"
            _LOGGER.info(message)
            raise ChatError(message=message, cause=e) from e

    @abstractmethod
    def handle_input_message(self, message: str):
        """
        Handles a message inputted from the user.

        :param message: The user's message.
        """

    @property
    def thread_id(self) -> str:
        """
        Return the thread id.

        :return: The thread id.
        """
        return self._thread_id

    @property
    def embedding_model(self) -> str:
        """
        Return the embedding model identifier.
        This is model used to embed vectors in the vectorstore.

        :return:  embedding model.
        """
        return self._embedding_model

    @property
    def hyper_parameters(self) -> dict:
        """
        Return internal hyper_parameters.

        :return: Parameters as a dict.
        """
        return self._hyper_parameters

    @property
    def chatbot(self) -> ChatOpenAI:
        """
        Return this handler's LLM Chatbot.

        :return: The LLM Chatbot for the handler.
        """
        return self._chatbot

    def retrieve_chatbot(
        self,
    ) -> ChatOpenAI:
        """
        Retrieve a chatbot based on model identifier.

        :return: A  `ChatOpenAI` instantiation with the model.
        """
        temperature = self.hyper_parameters.get("temperature", DEFAULT_MODEL_TEMP)
        # Some models require slightly different configurations.
        if self._model_url:
            _LOGGER.debug(f"Opening ChatOpenAI interface for model {self._llm_model}")
            llm = ChatOpenAI(
                temperature=temperature,
                model=self._llm_model,
                base_url=self._model_url,
                api_key=DEFAULT_OPEN_API_KEY,  # type: ignore
            )
        else:
            _LOGGER.debug(f"Opening ChatOpenAI interface for model {self._llm_model}")
            llm = ChatOpenAI(temperature=temperature, model=self._llm_model)
        return llm

    def _retrieve_vectors(self) -> VectorStoreRetriever:
        """
        Return a retriever for the vector store.

        :return: VectorStoreRetriever.
        """
        top_k = self.hyper_parameters.get("top_k", DEFAULT_TOP_K)
        _LOGGER.debug("Retrieving vector store retriever")
        return self._vector_store.db_client.as_retriever(search_kwargs={"k": top_k})

    def _create_workflow(self) -> StateGraph:
        """
        Create the workflow for the chatbot.

        :return: A `StateGraph` instance.
        """
        _LOGGER.info("Building State Graph")
        workflow = StateGraph(state_schema=MessagesState)
        workflow.add_node("model", self.rag_model)
        workflow.add_edge(START, "model")
        return workflow

    # Define the function that calls the chatbot LLM model.
    def _invoke_chatbot(self, state: MessagesState):
        """
        Invoke the chatbot model.

        :param state: Current message history.
        :return: Chat response.
        """
        return self.chatbot.invoke(state["messages"])

    def rag_model(self, state: MessagesState) -> dict:
        """
        Invoke the RAG model.

        :param state: Current message history.
        :return: Chat response.
        """
        response = self.chatbot.invoke(state["messages"])
        return {"messages": [response]}


class BabylonChatHandler(ChatHandler):
    """
    ChatHandler implementation for Babylon.
    """

    def __init__(
        self,
        embedding_model: str,
        llm_model: str,
        model_url: str | None = None,
        thread_id: str | None = None,
    ):
        """
        Constructor.

        :param embedding_model: Target embeddings model.
        :param llm_model: Target chatbot model.
        :param model_url: Model url.
        :param thread_id: Any predifined thread a current process is running on.
        """
        super().__init__(
            embedding_model=embedding_model,
            llm_model=llm_model,
            model_url=model_url,
            thread_id=thread_id,
        )

    def handle_input_message(self, message: str) -> Iterator:
        """
        Handle a user's input message.

        :param message: The user message.
        :return: Iterator over message responses.
        """
        input_message = HumanMessage(content=message)
        _LOGGER.debug(f"Generating streamed response for message: {message}")
        return self._app.stream(
            {"messages": [input_message]},  # type: ignore
            self._config,  # type: ignore
            stream_mode="values",
        )
