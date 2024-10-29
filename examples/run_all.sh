#!/bin/bash

OPTS=""
if [ -n "$2" ]; then
    OPTS="-u $2"
fi

for f in *.py
do
    python $f --key $1 "$OPTS"
done
