#!/bin/bash

if [ ! -d ".cache" ]; then
    mkdir .cache
fi

if [ ! -d ".cache/arxiv" ]; then
    mkdir .cache/arxiv
fi

if [ ! -d ".cache/prompts" ]; then
    mkdir .cache/prompts
fi

if [[ ! -e ".cache/store.db3" ]]; then

    sqlite3 .cache/store.db3 <<EOF
CREATE TABLE IF NOT EXISTS papers (
    arxiv_id TEXT PRIMARY KEY,
    title TEXT,
    summary TEXT
);

CREATE TABLE IF NOT EXISTS paper_references (
    arxiv_id TEXT,
    reference_title TEXT,
    PRIMARY KEY (arxiv_id, reference_title)
);

EOF

fi

cp ../textpy/compiler/prompts/_textpy_built_in_gen_* .cache/prompts

docker run \
    -v ./:/workspace \
    -v ./.cache:/cache \
    -w /workspace \
    -e DEEPSEEK_API_KEY=${DEEPSEEK_API_KEY} \
    textpy \
    python arxiv_search.py ${ARXIV_ID} /cache 3
