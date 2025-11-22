"""Controller for handling chat requests."""

import logging
from http import HTTPStatus
from typing import Any

import connexion
from flask import current_app
from langchain_core.messages import AIMessage
from oracle_server.handlers.handler import BabylonChatHandler, ChatHandler

_LOGGER = logging.getLogger()

# todo: move to config
DEFAULT_GPT_MODEL = "llama3.2"
DEFAULT_GPT_MODEL_URL = "http://localhost:11434/v1"


async def send_message(handler: str | None = None) -> tuple[dict[str, Any], int]:
    """
    Controller method for handling chat input.

    :param handler: Desired chat handler, identified by name.
    :return: Response from invoking chat handler.
    """
    request_body = await connexion.request.json()
    cfg = current_app.config
    thread_id = request_body.get("thread_id")
    chat_handler: ChatHandler = _select_handler(
        handler_name=handler, cfg=cfg, thread_id=thread_id
    )
    response_parts = []
    try:
        chat_response = chat_handler.handle_input_message(
            message=request_body["user_input"]
        )
        for event in chat_response:
            response_parts.append(_handle_chat_response(event=event))
    except Exception as e:
        message = f"Error while handling input message. {e}"
        _LOGGER.debug(message)
        return {"message": message}, HTTPStatus.INTERNAL_SERVER_ERROR

    response = "".join(response_parts)
    return {"text": response, "thread_id": chat_handler.thread_id}, HTTPStatus.OK


def _select_handler(handler_name: str | None, cfg: dict, thread_id: str) -> ChatHandler:
    """Return an appropriate handler."""
    # todo: add check for handler name.
    _LOGGER.info(f"handler name: {handler_name}")
    return BabylonChatHandler(
        llm_model=DEFAULT_GPT_MODEL,
        embedding_model=cfg["EMBEDDING_MODEL"],
        model_url=DEFAULT_GPT_MODEL_URL,
        thread_id=thread_id,
    )


def _handle_chat_response(event) -> str:
    """Handle chat response object and return the message content as a string."""
    _LOGGER.debug(f"Handling chat response event: {event}")
    try:
        last_message = event["messages"][-1]
        if not isinstance(last_message, AIMessage):
            return ""

        content = last_message.content

        if isinstance(content, str):
            return content

        if isinstance(content, list):
            return "".join(str(item) for item in content)

        return str(content)

    except (KeyError, IndexError, TypeError) as e:
        _LOGGER.info(f"Error handling chat response event: {event}. Error: {e}")
        return ""
