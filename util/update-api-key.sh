#!/bin/bash

newkey="$1"

rm alchemyapi_python/api_key.txt
python alchemyapi_python/alchemyapi.py "${newkey}"

rm scraper/api_key.txt
python scraper/alchemyapi.py "${newkey}"
