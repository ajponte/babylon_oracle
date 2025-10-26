# Note: This script is very much for dev/test purposes only.
"""Utils for interacting with Hashicorp/Openbao."""
from abc import ABC, abstractmethod
from typing import Any
import os
import logging
import hvac

_LOGGER = logging.getLogger()


class SecretsManagerException(Exception):
    """Throw this error for issues with a secrets manager."""

    def __init__(self, message: str, cause: Exception | None = None):
        """
        Constructor.

        :param message: Error message.
        :param cause: Optional throwable cause.
        """
        self._message = message
        self._cause = cause

    @property
    def message(self) -> str:
        """
        Return the message.

        :return: The message.
        """
        return self._message

    @property
    def cause(self) -> Exception | None:
        """
        Return the cause.

        :return: The cause.
        """
        return self._cause


class OpenBaoApiClient:
    """API client wrapper for OpenBao."""

    def __init__(self):
        """Constructor."""
        # todo: Add RSA cert
        self._client = hvac.Client(
            # `BAO_ADDR`, `VAULT_TOKEN` are the suggested env var names from Hashicorp.
            url=os.environ.get("BAO_ADDR", None),
            token=os.environ.get("VAULT_TOKEN", None),
        )
        self.__is_authenticated(self._client)
        _LOGGER.info("Hashicorp Secrets client authenticated.")

    # Testing for now. Needs to be removed for a production system.
    def add_secret_value(self, *, path: str, secret: dict) -> dict:
        """
        Writes the secret under `secrets/path`

        :param path: Secrets path.
        :param secret: Secret key/value pair as a dict.
        :return: The response from setting the secret in the vault.
        :raise: SecretsManagerException - Upon error.
        """
        try:
            create_response = self._client.secrets.kv.v2.create_or_update_secret(
                path=path, secret=secret
            )
            _LOGGER.info(f"Set secret value at path {path}")
            return create_response
        except Exception as e:
            message = f"Exception while setting secret value at path {path}"
            _LOGGER.exception(message)
            raise SecretsManagerException(message, cause=e) from e

    def read_secret_values(self, *, path: str) -> dict:
        """
        Reads secrets from the path.

        :param path: The secrets path to read from.
        :return: The read response data.
        :raise: SecretsManagerException - Upon error.
        """
        try:
            # todo: add version checking.
            read_response = self._client.secrets.kv.read_secret_version(
                path=path,
                # See https://github.com/hvac/hvac/pull/907
                raise_on_deleted_version=False,
            )["data"]
            ver = read_response["metadata"]["version"]
            _LOGGER.debug(f"Found secrets version: {ver}")
            _LOGGER.debug(f"Successfully read secrets from path {path}")
            return read_response["data"]
        except Exception as e:
            message = f"Exception while reading secret values at path {path}"
            _LOGGER.exception(message)
            raise SecretsManagerException(message, cause=e) from e

    @classmethod
    def __is_authenticated(cls, client: hvac.Client):
        """Return True only if the Client has been authenticated."""
        assert client.is_authenticated(), "Hashicorp is not authenticated!"


class AbstractSecretsManager(ABC):
    """Abstract implementation for a secrets manager."""

    @abstractmethod
    def add_secret(self, path: str, secret: dict) -> bool:
        """
        Add PATH/KEY to the internal secrets store.

        :param path: The path in the secrets store.
        :param secret: The secret kv.
        """

    @abstractmethod
    def get_secret(self, path: str, key: str) -> dict:
        """Fetch the secret value for PATH/KEY from the internal secrets store."""


class BaoSecretsManager(AbstractSecretsManager):
    """OpenBao implementation of `AbstractSecretsManager`."""
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(BaoSecretsManager, cls).__new__(cls)
            cls._instance._client = OpenBaoApiClient()
            cls._instance._cache = {}
        return cls._instance

    def add_secret(self, path: str, secret: dict) -> bool:
        response: dict = self._client.add_secret_value(
            path=path, secret=secret
        )
        if not response:
            _LOGGER.info("No response from client")
            return False
        # Invalidate cache for the path
        if path in self._cache:
            del self._cache[path]
        return True

    def get_secret(self, path: str, key: str) -> dict:
        if path not in self._cache:
            _LOGGER.info(f"Secrets under {path} not cached.")
            secrets = self._client.read_secret_values(path=path)
            if not secrets:
                raise SecretsManagerException(f"No secrets returned under path {path}")
            self._cache[path] = secrets

        secrets = self._cache[path]
        if key not in secrets:
            raise SecretsManagerException(f"Secret {path}/{key} not found.")
        return {"key": key, "val": secrets[key]}
