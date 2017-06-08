#!/bin/bash

source ./venv/bin/activate

export YOURAPPLICATION_SETTINGS=/var/www/eatpotmovie-ci/config.py

pip3 install -r requirements.txt

python3 managy.py db init

python3 managy.py db migrate -m "initial migration"

python3 managy.py db upgrade

exit 0
