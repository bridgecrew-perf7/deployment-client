#!/usr/bin/env bash
export PYTHONPATH=$PWD
pipenv run gunicorn -b 0.0.0.0:8003 --log-level=DEBUG --workers=1 --timeout=90 'dclient.app:create_app'
