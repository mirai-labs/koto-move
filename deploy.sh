#!/bin/bash

NETWORK=$1

mv ./Move.${NETWORK}.toml ./Move.toml
NETWORK=${NETWORK} python ./publish.py
mv ./Move.toml ./Move.${NETWORK}.toml