#!/bin/bash

if [ ! -d ".cache" ]; then
    mkdir .cache
fi

cp ../textpy/compiler/prompts/_textpy_built_in_gen_* .cache/

docker run \
    -v ./:/workspace \
    -v ./.cache:/cache \
    -w /workspace \
    -e DEEPSEEK_API_KEY=${DEEPSEEK_API_KEY} \
    textpy \
    python arxiv_search.py ${ARXIV_ID} /cache/arxiv/