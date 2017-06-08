#!/bin/bash

uwsgi -s /tmp/eatpotmovie-ci.sock --manage-script-name --mount /=managy:app --plugin python3 --virtualenv ./venv/

exit 0
