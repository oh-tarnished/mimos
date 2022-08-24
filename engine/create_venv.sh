#!/bin/bash

python3.10 -m pip install --user virtualenv
python3.10 -m virtualenv venv && source ./venv/bin/activate && pip install -r ./requirements.txt
