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
    handler = BabylonChatHandler(
        llm_model=DEFAULT_GPT_MODEL,
        embedding_model=cfg['EMBEDDING_MODEL']
    )
    response = ''
    try:
        chat_response = handler.handle_input_message(message=request_body['user_input'])
        for event in chat_response:
            response += event["messages"][-1]
    except Exception as e:
        message = f'Error while handling input message. {e}'
        _LOGGER.debug(message)
        return {'message': message}, HTTPStatus.INTERNAL_SERVER_ERROR

    return {'text': response}, HTTPStatus.OK
