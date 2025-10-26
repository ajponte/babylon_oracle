from http import HTTPStatus
from typing import Any


async def send_message(handler: str | None = None) -> tuple[dict[str, Any], int]:
    print(f'Registered handler: {handler}')
    return {'text': 'I am a dumb server'}, HTTPStatus.OK
