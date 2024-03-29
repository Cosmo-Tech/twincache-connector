# Copyright (c) Cosmo Tech corporation.
# Licensed under the MIT license.
import logging
import time

from CosmoTech_Acceleration_Library.Modelops.core.io.model_exporter import ModelExporter

logger = logging.getLogger(__name__)


class TwinCacheConnector:
    """
    Connector class to export data from twin cache solution into csv files
    """

    def __init__(self,
                 twin_cache_host: str,
                 twin_cache_port: int,
                 twin_cache_name: str,
                 twin_cache_password: str = None,
                 export_path: str = "/"):
        self.twin_cache_host = twin_cache_host
        self.twin_cache_port = twin_cache_port
        self.twin_cache_name = twin_cache_name
        self.export_path = export_path
        self.m_exporter = ModelExporter(host=twin_cache_host,
                                        port=twin_cache_port,
                                        name=twin_cache_name,
                                        password=twin_cache_password,
                                        export_dir=export_path)

    def run(self, filtering_queries: list = None):
        """
        Export all data from twin cache instance
        """
        logger.debug("Start export job...")
        export_job_start = time.time()
        if filtering_queries:
            self.m_exporter.export_from_queries(filtering_queries)
        else:
            self.m_exporter.export_all_data()

        export_job_timing = time.time() - export_job_start
        logger.debug(f"Export job took : {export_job_timing} s")
