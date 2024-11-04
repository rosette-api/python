#!/bin/bash

if [ $# -eq 0 ]; then
    echo "Usage: $0 API_KEY [ALT_URL]" 1>&2
    exit 1
fi

for f in *.py
do
  if [ -n "$2" ]; then
    python $f --key $1 --url $2
  else
    python $f --key $1
  fi
done
