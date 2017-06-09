#!/bin/bash

if [ "$YOURAPPLICATION_SETTINGS" = "" ]; then
    echo "Env var YOURAPPLICATION_SETTINGS not set, exit..."
    exit 1
fi

uwsgi -s /tmp/eatpotmovie-ci.sock --manage-script-name --mount /=managy:app --virtualenv ./venv/

exit 0
