import unittest
from unittest.mock import patch, Mock

from oracle_server.handlers.handler import BabylonChatHandler


class TestBabylonChatHandler(unittest.TestCase):

    @patch('oracle_server.handlers.handler.ChromaVectorStore')
    @patch('oracle_server.handlers.handler.ChatOpenAI')
    @patch('oracle_server.handlers.handler.StateGraph')
    @patch('oracle_server.handlers.handler.MemorySaver')
    def setUp(self, mock_memory_saver, mock_state_graph, mock_chat_openai, mock_vector_store):
        self.mock_memory_saver = mock_memory_saver
        self.mock_state_graph = mock_state_graph
        self.mock_chat_openai = mock_chat_openai
        self.mock_vector_store = mock_vector_store

        self.mock_app = Mock()
        self.mock_workflow = Mock()
        self.mock_workflow.compile.return_value = self.mock_app
        self.mock_state_graph.return_value = self.mock_workflow

        self.handler = BabylonChatHandler(
            embedding_model="test_embedding_model",
            llm_model="test_llm_model",
            model_url="http://test.url"
        )

    def test_handle_input_message(self):
        # Arrange
        message = "Hello, world!"
        
        # Act
        self.handler.handle_input_message(message)

        # Assert
        self.mock_app.stream.assert_called_once()
        args, kwargs = self.mock_app.stream.call_args
        self.assertEqual(len(args), 2)
        self.assertEqual(len(kwargs), 1)

        # Check the inputs to the stream
        input_messages = args[0].get("messages")
        self.assertEqual(len(input_messages), 1)
        self.assertEqual(input_messages[0].content, message)
        self.assertEqual(kwargs.get("stream_mode"), "values")
