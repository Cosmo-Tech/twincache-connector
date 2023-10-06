# Copyright (c) Cosmo Tech corporation.
# Licensed under the MIT license.
import logging
import os
import sys
import cosmotech_api
import json
from cosmotech_api.api import scenario_api
from cosmotech_api.model.scenario import Scenario
from azure.identity import DefaultAzureCredential

from TwinCache_Connector.twincache_connector import TwinCacheConnector
from auth.authentication import Authentication

main_logger_name = "TwinCacheConnector_main"

env_var_required = ["TWIN_CACHE_HOST", "TWIN_CACHE_PORT", "TWIN_CACHE_NAME", "CSM_FETCH_ABSOLUTE_PATH"]

log_level_name = os.getenv("LOG_LEVEL") if "LOG_LEVEL" in os.environ else "INFO"
log_level = logging.getLevelName(log_level_name)
logging.basicConfig(stream=sys.stdout,
                    level=log_level,
                    format='%(levelname)s(%(name)s) - %(asctime)s - %(message)s',
                    datefmt='%d-%m-%y %H:%M:%S')
logger = logging.getLogger(__name__)


def check_env_var():
    """
    Check if all required environment variables are specified
    """
    for env_var in env_var_required:
        if env_var not in os.environ:
            yield env_var


def create_connector() -> TwinCacheConnector:
    missing_env_vars = list(check_env_var())
    if missing_env_vars:
        raise Exception(f"Missing environment variables named {missing_env_vars}")

    twin_cache_host = os.getenv("TWIN_CACHE_HOST")
    twin_cache_port = os.getenv("TWIN_CACHE_PORT")
    twin_cache_name = os.getenv("TWIN_CACHE_NAME")
    twin_cache_password = os.getenv("TWIN_CACHE_PASSWORD")
    export_path = os.path.join(os.getenv("CSM_FETCH_ABSOLUTE_PATH"), '')

    logger.debug("twin_cache_host %s", twin_cache_host)
    logger.debug("twin_cache_port %s", twin_cache_port)
    logger.debug("twin_cache_name %s", twin_cache_name)
    return TwinCacheConnector(twin_cache_host=twin_cache_host,
                              twin_cache_port=int(twin_cache_port),
                              twin_cache_name=twin_cache_name,
                              twin_cache_password=twin_cache_password,
                              export_path=export_path)


def get_parametered_queries() -> list:
    twin_cache_filtering_queries = os.getenv("SUBSET_QUERY")
    logger.debug(f'Filtering queries receved: {twin_cache_filtering_queries}')
    if twin_cache_filtering_queries:
        return twin_cache_filtering_queries.split(';')

    twin_cache_filtering_queries_name = os.getenv("SCENARIO_SUBSET_QUERY_NAME")
    logger.debug("twin_cache_filtering_queries_name %s", twin_cache_filtering_queries_name)
    if twin_cache_filtering_queries_name:
        # get query parameters
        default_cred = Authentication(os.getenv('IDENTITY_PROVIDER'))
        configuration = cosmotech_api.Configuration(host=os.getenv('CSM_API_URL'),
                                                    discard_unknown_keys=True,
                                                    access_token=default_cred.get_token(
                                                        os.getenv('CSM_API_SCOPE')))

        with cosmotech_api.ApiClient(configuration) as api_client:
            api_instance = scenario_api.ScenarioApi(api_client)
            scenario = api_instance.find_scenario_by_id(os.getenv('CSM_ORGANIZATION_ID'), os.getenv('CSM_WORKSPACE_ID'),
                                                        os.getenv('CSM_SCENARIO_ID'))

        _match = [
            p.value for p in scenario.parameters_values if p.parameter_id == os.getenv('SCENARIO_SUBSET_QUERY_NAME')
        ]

        if len(_match) == 1:
            if _match[0]:
                twin_cache_filtering_queries = json.loads(_match[0])
                return twin_cache_filtering_queries
            else:
                # parameter existe but empty
                return []
        elif len(_match) == 0:
            # No parameter found back to default run
            return []
        else:
            raise RuntimeError(
                f"Multiple parameter {os.getenv('SCENARIO_SUBSET_QUERY_NAME')} found in scenario parameters")
    else:
        return []


if __name__ == "__main__":
    twincache_connector = create_connector()
    twincache_connector.run(get_parametered_queries())
