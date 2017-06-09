#!/bin/bash

uwsgi -s /tmp/eatpotmovie-ci.sock --manage-script-name --mount /=managy:app --virtualenv ./venv/

exit 0
