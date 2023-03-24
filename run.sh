#!/bin/bash

export MODE=d
export MAX_MODELS=20000
export JSON_FILE='_data/lustrous/raw/vroid/metadata.json'
source ./_env/vroid_cookie.bashrc

docker-compose up

docker-compose down



