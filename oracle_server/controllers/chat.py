"""Controller for handling chat requests."""
import logging
from http import HTTPStatus
from typing import Any

import connexion
from flask import current_app
from oracle_server.handlers.handler import BabylonChatHandler

_LOGGER = logging.getLogger()

# todo: move to config
DEFAULT_GPT_MODEL = 'llama3.2'
DEFAULT_GPT_MODEL_URL = 'http://localhost:11434/v1'


async def send_message(handler: str | None = None) -> tuple[dict[str, Any], int]:
    print(f'Registered handler: {handler}')
    request_body = await connexion.request.json()
    cfg = current_app.config
    thread_id = request_body.get('thread_id')
    handler = BabylonChatHandler(
        llm_model=DEFAULT_GPT_MODEL,
        embedding_model=cfg['EMBEDDING_MODEL'],
        model_url=DEFAULT_GPT_MODEL_URL,
        thread_id=thread_id
    )
    response = ''
    try:
        chat_response = handler.handle_input_message(message=request_body['user_input'])
        for event in chat_response:
            response += event["messages"][-1].content
    except Exception as e:
        message = f'Error while handling input message. {e}'
        _LOGGER.debug(message)
        return {'message': message}, HTTPStatus.INTERNAL_SERVER_ERROR

    return {'text': response, 'thread_id': handler.thread_id}, HTTPStatus.OK
