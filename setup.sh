#!/bin/bash

# install dependencies
pip install setuptools
pip install -r requirements.txt

# Run django commands
py manage.py makemigrations
py manage.py migrate
py manage.py collectstatic
py manage.py 