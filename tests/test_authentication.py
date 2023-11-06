import os
from auth import authentication
from unittest.mock import patch
import pytest
import requests


def test_get_token_not_supported():
    authent = authentication.Authentication('not_supported_identity_provider')
    with pytest.raises(Exception) as e:
        authent.get_token('scope')
        assert str(e) == 'identity provider not_supported_identity_provider not supported'


@pytest.fixture
def okta_env_vars():
    os.environ['OKTA_CLIENT_ID'] = 'okta_client_id'
    os.environ['OKTA_CLIENT_SECRET'] = 'okta_client_secret'
    os.environ['OKTA_CLIENT_ISSUER'] = 'okta_client_issuer'
    yield
    os.environ.pop('OKTA_CLIENT_ID')
    os.environ.pop('OKTA_CLIENT_SECRET')
    os.environ.pop('OKTA_CLIENT_ISSUER')


@patch('requests.post')
def test_get_okta_token(mock_post, okta_env_vars):
    mock_post.return_value.status_code = requests.codes.ok
    mock_post.return_value.json.return_value = {'access_token': 'okta_token'}

    authent = authentication.Authentication('okta')
    token = authent.get_token('scope')

    assert token == 'okta_token'


@patch('requests.post')
def test_get_okta_token_error(mock_post, okta_env_vars):
    mock_post.return_value.status_code = requests.codes.bad_request

    authent = authentication.Authentication('okta')
    with pytest.raises(Exception) as e:
        authent.get_token('scope')
        assert str(e) == 'error'


@patch('azure.identity.DefaultAzureCredential.get_token')
def test_get_azure_token(mock_get_token):
    mock_get_token.return_value.token = 'azure_token'

    authent = authentication.Authentication('azure')
    token = authent.get_token('scope')

    assert token == 'azure_token'
