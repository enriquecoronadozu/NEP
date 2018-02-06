#!/usr/bin/env bash

# This script is used for build the NEP libraries


echo Installing  third party libraries ...

python -m pip install --upgrade pip
pip install zmq
pip install tinydb
pip install simplejson

echo Building NEP libraries and packages

python make_nep.py
python make_packages.py

