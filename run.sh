# Copyright (c) Cosmo Tech corporation.
# Licensed under the MIT license.

set -x

docker run \
--network="host" \
-e TWIN_CACHE_HOST="$(printenv TWIN_CACHE_HOST)" \
-e TWIN_CACHE_NAME="$(printenv TWIN_CACHE_NAME)" \
-e TWIN_CACHE_PORT="$(printenv TWIN_CACHE_PORT)" \
-e TWIN_CACHE_PASSWORD="$(printenv TWIN_CACHE_PASSWORD)" \
-e CSM_FETCH_ABSOLUTE_PATH="$(printenv CSM_FETCH_ABSOLUTE_PATH)" \
-v "$(printenv CSM_FETCH_ABSOLUTE_PATH)":"$(printenv CSM_FETCH_ABSOLUTE_PATH)" \
-e LOG_LEVEL="INFO" \
twincache-connector
