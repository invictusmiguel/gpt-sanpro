#!/bin/bash

python3 -m ensurepip --upgrade
python3 -m pip install --upgrade pip setuptools wheel --no-cache-dir
python3 -m pip install -r requirements.txt --no-cache-dir
