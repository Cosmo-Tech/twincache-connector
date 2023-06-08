# Cosmo Tech Twin Cache connector

The aim of this project is to read data from Cosmo Tech Twin Cache solution

#### Features

- Read data from Cosmo Tech Twin Cache solution regarding environment variables
- Export data in several CSV files 
- Metrics logging

## Environment variables :

Here is the list of environment variables:

- **TWIN_CACHE_HOST**: the twin cache host
- **TWIN_CACHE_PORT**: the twin cache port
- **TWIN_CACHE_NAME**: the twin cache key name where data will be stored
- **TWIN_CACHE_PASSWORD**: the twin cache password udes to read data
- **CSM_FETCH_ABSOLUTE_PATH**: defined the CSV files export path

## Log level

Default log level defined is "INFO".
We use the logging API [logging](https://docs.python.org/3/library/logging.html).
You can change the log level by setting an environment variable named: **LOG_LEVEL**.
Log levels used for identifying the severity of an event. Log levels are organized from most specific to least:

- CRITICAL
- ERROR
- WARNING
- INFO
- DEBUG
- NOTSET

## How to run your image locally

### Build the docker image

`docker build -t twincache-connector .`

### Run the docker image

Fill the following command with your information:

```
export TWIN_CACHE_HOST=<twin_cache_host>
export TWIN_CACHE_NAME=<twin_cache_name>
export TWIN_CACHE_PORT=<twin_cache_port>
export TWIN_CACHE_PASSWORD=<twin_cache_port>
export CSM_FETCH_ABSOLUTE_PATH=<export_path>
```

Then run:

`./run.sh`

**N.B:**

- Default log level is set to 'info'

## Tasks :

- [ ]  Handle username/password for secured twin cache connection
