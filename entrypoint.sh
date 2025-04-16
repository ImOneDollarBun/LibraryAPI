#!/bin/bash

python app/utils/certs/gen_keys.py

exec python main.py
