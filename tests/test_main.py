import os
import pytest
from unittest.mock import patch
import main
import cosmotech_api
import auth


@patch('main.TwinCacheConnector')
def test_main_no_var_env(mock_twin_cache_connector):
    with pytest.raises(Exception) as exc_info:
        main.create_connector()
    assert exc_info.value.args[0] == ("Missing environment variables named ['TWIN_CACHE_HOST', "
                                      "'TWIN_CACHE_PORT', 'TWIN_CACHE_NAME', 'CSM_FETCH_ABSOLUTE_PATH']")


@pytest.fixture
def var_env():
    os.environ['TWIN_CACHE_HOST'] = 'localhost'
    os.environ['TWIN_CACHE_PORT'] = '6379'
    os.environ['TWIN_CACHE_NAME'] = 'test'
    os.environ['CSM_FETCH_ABSOLUTE_PATH'] = '/tmp'


@patch('main.TwinCacheConnector')
def test_main(mock_twin_cache_connector, var_env):
    main.create_connector()


def test_get_parametered_queries_no_env_var():
    queries = main.get_parametered_queries()
    assert queries == []


@pytest.fixture
def queries_var_env():
    os.environ['SCENARIO_SUBSET_QUERY_NAME'] = 'scenario_subset'


@patch('cosmotech_api.api.scenario_api.ScenarioApi')
@patch('auth.authentication.Authentication.get_token')
def test_get_parametered_queries_with_empty_env_var(mock_auth, mock_scenario_api, queries_var_env):
    # create scenario parameter value
    scenario_parameter_values = cosmotech_api.model.scenario_run_template_parameter_value.ScenarioRunTemplateParameterValue(
        parameter_id="scenario_subset", value="")

    # create scenario
    scenario = cosmotech_api.model.scenario.Scenario()
    scenario.parameters_values = [scenario_parameter_values]

    # mock scenario api instance
    api_instance = mock_scenario_api.return_value
    api_instance.find_scenario_by_id.return_value = scenario

    queries = main.get_parametered_queries()
    assert queries == []


@patch('cosmotech_api.api.scenario_api.ScenarioApi')
@patch('auth.authentication.Authentication.get_token')
def test_get_parametered_queries_with_env_var(mock_auth, mock_scenario_api, queries_var_env):
    # create scenario parameter value
    scenario_parameter_values = cosmotech_api.model.scenario_run_template_parameter_value.ScenarioRunTemplateParameterValue(
        parameter_id="scenario_subset", value="[\"query1\", \"query2\"]")

    # create scenario
    scenario = cosmotech_api.model.scenario.Scenario()
    scenario.parameters_values = [scenario_parameter_values]

    # mock scenario api instance
    api_instance = mock_scenario_api.return_value
    api_instance.find_scenario_by_id.return_value = scenario

    queries = main.get_parametered_queries()
    assert queries == ['query1', 'query2']


@patch('cosmotech_api.api.scenario_api.ScenarioApi')
@patch('auth.authentication.Authentication.get_token')
def test_get_parametered_queries_with_too_many_matching_env_var(mock_auth, mock_scenario_api, queries_var_env):
    # create scenario parameter value
    scenario_parameter_values_1 = cosmotech_api.model.scenario_run_template_parameter_value.ScenarioRunTemplateParameterValue(
        parameter_id="scenario_subset", value="[\"query1\", \"query2\"]")
    scenario_parameter_values_2 = cosmotech_api.model.scenario_run_template_parameter_value.ScenarioRunTemplateParameterValue(
        parameter_id="scenario_subset", value="[\"query3\", \"query4\"]")

    # create scenario
    scenario = cosmotech_api.model.scenario.Scenario()
    scenario.parameters_values = [scenario_parameter_values_1, scenario_parameter_values_2]

    # mock scenario api instance
    api_instance = mock_scenario_api.return_value
    api_instance.find_scenario_by_id.return_value = scenario

    with pytest.raises(Exception) as exc_info:
        main.get_parametered_queries()
    assert exc_info.value.args[0] == "Multiple parameter scenario_subset found in scenario parameters"


@pytest.fixture
def empty_queries_var_env():
    os.environ['SCENARIO_SUBSET_QUERY_NAME'] = ''


@patch('cosmotech_api.api.scenario_api.ScenarioApi')
def test_get_parametered_queries_with_env_var_empty(mock_scenario_api, empty_queries_var_env):
    # create scenario parameter value
    scenario_parameter_values = cosmotech_api.model.scenario_run_template_parameter_value.ScenarioRunTemplateParameterValue(
        parameter_id="scenario_subset", value="[\"query1\", \"query2\"]")

    # create scenario
    scenario = cosmotech_api.model.scenario.Scenario()
    scenario.parameters_values = [scenario_parameter_values]

    # mock scenario api instance
    api_instance = mock_scenario_api.return_value
    api_instance.find_scenario_by_id.return_value = scenario

    queries = main.get_parametered_queries()
    assert queries == []


@patch('cosmotech_api.api.scenario_api.ScenarioApi')
@patch('auth.authentication.Authentication.get_token')
def test_get_parametered_queries_with_env_var_not_found(mock_auth, mock_scenario_api, queries_var_env):
    # create scenario parameter value
    scenario_parameter_values = cosmotech_api.model.scenario_run_template_parameter_value.ScenarioRunTemplateParameterValue(
        parameter_id="scenario_noTheRightName", value="[\"query1\", \"query2\"]")

    # create scenario
    scenario = cosmotech_api.model.scenario.Scenario()
    scenario.parameters_values = [scenario_parameter_values]

    # mock scenario api instance
    api_instance = mock_scenario_api.return_value
    api_instance.find_scenario_by_id.return_value = scenario

    queries = main.get_parametered_queries()
    assert queries == []
