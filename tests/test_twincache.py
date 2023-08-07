import pytest
from unittest.mock import patch
from TwinCache_Connector.twincache_connector import TwinCacheConnector


@patch('TwinCache_Connector.twincache_connector.ModelMetadata')
@patch('TwinCache_Connector.twincache_connector.ModelExporter')
def test_twincache_main(mock_model_exporter, mock_model_metadata):
    twincache = TwinCacheConnector('host', 3333, 'name')
    twincache.run()
    twincache.m_exporter.export_all_data.assert_called_once()


@patch('TwinCache_Connector.twincache_connector.ModelMetadata')
@patch('TwinCache_Connector.twincache_connector.ModelExporter')
def test_twincache_with_queries(mock_model_exporter, mock_model_metadata):
    twincache = TwinCacheConnector('host', 3333, 'name')
    twincache.run(['query1', 'query2'])
    twincache.m_exporter.export_from_queries.assert_called_once_with(['query1', 'query2'])
