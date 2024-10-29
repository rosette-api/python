#!/bin/bash

if [ $# -eq 0 ]; then
    echo "Usage: $0 API_KEY [ALT_URL]" 1>&2
    exit 1
fi
OPTS=""
if [ -n "$2" ]; then
    OPTS="-u $2"
fi

for f in *.py
do
    python $f --key $1 "$OPTS"
done
