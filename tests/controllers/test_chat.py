import uuid
from unittest.mock import patch, MagicMock

BASE_URI = '/api'


def test_chat(app_client):
    uri = f'{BASE_URI}/message'
    body = {
        'user_input': 'hello'
    }

    # Create a mock response that simulates the generator behavior
    mock_chat_response = [
        {"messages": [MagicMock(content="I am a dumb server")]}
    ]

    with patch('oracle_server.controllers.chat.BabylonChatHandler') as mock_handler:
        # Configure the instance's method to return the mock response
        mock_handler.return_value.handle_input_message.return_value = mock_chat_response
        mock_handler.return_value.thread_id = uuid.uuid4().hex

        resp = app_client.post(uri, json=body)

        assert resp.status_code == 200
        json_data = resp.json()
        assert json_data['text'] == 'I am a dumb server'

