# MaxLog

Log data to a time database.
Read logged data to a csv file.

## Setup

From the main directory, run bash setup.sh.
This script will setup the docker container with influxdb,
create a python environment,
install python requirements.

## Usage

After completing the setup,
start the logging scripts you require.
All the logging scripts will send their data to the database with the actual timestamp for reference.
After you captured all data of one measurement,
start the export script,
to export all data of the database to one combined csv file,
the export script will then clear all data from the database for a new start.

## Cleaning up

Run bash remove.sh to clean up the python environment
and the docker container
and all the docker volumes
after usage.
Be careful since this will remove all containers and volumes named influxdb.
