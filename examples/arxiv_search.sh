#!/bin/bash

docker pull ghcr.io/yezhengmao1/textpy:latest

docker run \
    -v ./:/workspace \
    -w /workspace \
    -p 31108:31108 \
    -e DEEPSEEK_API_KEY=${DEEPSEEK_API_KEY} \
    ghcr.io/yezhengmao1/textpy:latest \
    python arxiv_search.py ${ARXIV_ID} ${CACHE_DIR} 3
