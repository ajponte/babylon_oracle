import oracle_server.config.hashicorp as MUT
from pytest import fixture
from unittest.mock import ANY, patch

# Mock secrets to be used in tests
MOCK_SECRETS = {
    'k1': 's1',
    'k2': 's2'
}


def test_open_bao_api_client_read_secrets(hvac_client):
    """
    Tests reading secrets from the OpenBaoApiClient by mocking the underlying
    hvac.Client and its methods.
    """
    # Configure the mock instance's methods to return the expected values
    hvac_client.return_value.is_authenticated.return_value = True
    hvac_client.return_value.secrets.kv.read_secret_version.return_value = {
        'data': {
            'data': MOCK_SECRETS,
            'metadata': {'version': 1}
        }
    }

    # Instantiate the client, which will use our mocked hvac client
    api_client = MUT.OpenBaoApiClient()

    # Call the method under test
    secrets = api_client.read_secret_values(path=ANY)

    # Assert the method was called correctly on the mock client
    hvac_client.return_value.secrets.kv.read_secret_version.assert_called_with(
        path=ANY,
        raise_on_deleted_version=False
    )

    # Assert the returned data matches the mock secrets
    assert secrets == MOCK_SECRETS


def test_open_bao_api_client_add_secret(hvac_client):
    """
    Tests adding a secret using the OpenBaoApiClient.
    """
    mock_add_response = {'data': {'foo': 'bar'}}

    # Configure the mock for the add method
    hvac_client.return_value.is_authenticated.return_value = True
    hvac_client.return_value.secrets.kv.v2.create_or_update_secret.return_value = mock_add_response

    # Instantiate the client
    api_client = MUT.OpenBaoApiClient()

    secret_to_add = {'foo': 'bar'}
    path = 'test_add_path'

    # Call the method under test
    response = api_client.add_secret_value(path=path, secret=secret_to_add)

    # Assert the method was called correctly
    hvac_client.return_value.secrets.kv.v2.create_or_update_secret.assert_called_with(
        path=path,
        secret=secret_to_add
    )

    # Assert the response matches the mocked response
    assert response == mock_add_response


@fixture
def bao_secrets_manager():
    """Fixture to provide a BaoSecretsManager instance for testing."""
    # By patching the OpenBaoApiClient, we can control its behavior in tests
    with patch('oracle_server.config.hashicorp.OpenBaoApiClient') as mock_api_client:
        # We need to clear the singleton instance to ensure a fresh start for each test
        MUT.BaoSecretsManager._instance = None
        MUT.BaoSecretsManager._initialized = False
        manager = MUT.BaoSecretsManager()
        # We replace the manager's client with our mock
        manager._client = mock_api_client
        yield manager


def test_bao_secrets_manager_add_secret(bao_secrets_manager):
    """
    Tests the add_secret method of the BaoSecretsManager.
    """
    path = 'test_path'
    secret = {'key': 'value'}
    bao_secrets_manager._client.add_secret_value.return_value = {'data': 'some_response'}

    # Call the method under test
    result = bao_secrets_manager.add_secret(path=path, secret=secret)

    # Assert the underlying client method was called correctly
    bao_secrets_manager._client.add_secret_value.assert_called_with(path=path, secret=secret)
    assert result is True


def test_bao_secrets_manager_get_secret_from_api_and_cache(bao_secrets_manager):
    """
    Tests the get_secret method of the BaoSecretsManager, including caching.
    """
    path = 'test_path'
    key = 'k1'
    bao_secrets_manager._client.read_secret_values.return_value = MOCK_SECRETS

    # First call, should fetch from API
    secret = bao_secrets_manager.get_secret(path=path, key=key)

    # Assert the underlying client method was called
    bao_secrets_manager._client.read_secret_values.assert_called_with(path=path)
    assert secret == {'key': key, 'val': MOCK_SECRETS[key]}

    # Reset the mock to test caching
    bao_secrets_manager._client.read_secret_values.reset_mock()

    # Second call, should use cache
    secret_from_cache = bao_secrets_manager.get_secret(path=path, key=key)

    # Assert the underlying client method was NOT called again
    bao_secrets_manager._client.read_secret_values.assert_not_called()
    assert secret_from_cache == {'key': key, 'val': MOCK_SECRETS[key]}