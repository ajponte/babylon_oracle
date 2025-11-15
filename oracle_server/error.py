"""Domain-level errors."""

class ChatError(Exception):
    """
    Throw this error when there's an issue handling chat messages.
    """

    def __init__(self, message: str, cause: Exception | None = None):
        """
        Constructor.

        :param message: Custom message.
        :param cause: Optional cause.
        """
        self._message = message
        self._cause = cause

    @property
    def message(self) -> str:
        """
        Return the custom message.

        :return: The message.
        """
        return self._message

    @property
    def cause(self) -> Exception | None:
        """
        Return the cause of this error.

        :return: The exception cause.
        """
        return self._cause


class VectorDBError(Exception):
    """
    Throw this error when there's an issue operating on a vector database.
    """

    def __init__(self, message: str, cause: Exception | None = None):
        """
        Constructor.

        :param message: Custom message.
        :param cause: Optional cause.
        """
        self._message = message
        self._cause = cause

    @property
    def message(self) -> str:
        """
        Return the custom message.

        :return: The message.
        """
        return self._message

    @property
    def cause(self) -> Exception | None:
        """
        Return the cause of this error.

        :return: The exception cause.
        """
        return self._cause
