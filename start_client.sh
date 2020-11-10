#!/usr/bin/env bash

pipenv run gunicorn -b 0.0.0.0:8003 --log-level=INFO --workers=1 --timeout=90 'dclient.app:app'
