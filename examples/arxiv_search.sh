#!/bin/bash

docker run \
    -v ./:/workspace \
    -v ./.cache:/cache \
    -w /workspace \
    -e DEEPSEEK_API_KEY=${DEEPSEEK_API_KEY} \
    textpy \
    python arxiv_search.py ${ARXIV_URL} /cache/arxiv/