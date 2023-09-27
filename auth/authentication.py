import os
import base64
import requests
from azure.identity import DefaultAzureCredential


class Authentication:
    """This class abstract authentication for cosmotech api. it use environement variable given by the api to create matching authentication."""

    def __init__(self, identity_provider: str):
        self.identity_provider = identity_provider

    def get_token(self, scope):
        if self.identity_provider == 'okta':
            return self._get_okta_token(scope)
        elif self.identity_provider == 'azure':
            return self._get_azure_token(scope)
        else:
            raise RuntimeError(f"identity provider '{self.identity_provider}' not supported")

    def _get_okta_token(self, scope):
        clientId = os.environ['OKTA_CLIENT_ID']
        clientSecret = os.environ['OKTA_CLIENT_SECRET']
        basic_token = base64.b64encode(f'{clientId}:{clientSecret}'.encode('utf-8')).decode('utf-8')

        issuer = os.environ['OKTA_CLIENT_ISSUER']

        headers = {'authorization': f'Basic {basic_token}'}
        payload = {'grant_type': 'client_credentials', 'scope': scope}
        response = requests.post(url=f'{issuer}/v1/token', headers=headers, data=payload)
        json_response = response.json()
        if response.status_code != requests.codes.ok:
            raise RuntimeError(f'{json_response["error"]}: {json_response["error_description"]}')
        return json_response['access_token']

    def _get_azure_token(self, scope):
        default_cred = DefaultAzureCredential()
        return default_cred.get_token(scope).token
