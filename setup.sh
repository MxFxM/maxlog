#!/bin/bash

echo "checking for docker"
echo "running docker compose"
cd ./setup
docker-compose up -d
cd ..

echo "creating influx credentials"

echo "creating python environment"
python3 -m venv python_environment

echo "activating python environment"
source ./python_environment/bin/activate

echo "installing python requirements"
python3 -m pip install -r ./setup/python_requirements.txt
