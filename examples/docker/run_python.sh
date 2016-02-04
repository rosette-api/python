#!/bin/bash

# reference the API 
curl "https://api.rosette.com/rest/v1/ping" -H "user_key: $1"

cp /source/*.* .

if [ ! -z "$2" ]; then
    find -maxdepth 1  -name '*.py' -print -exec tox -- {} --key $1 --url $2 \;
else
	find -maxdepth 1  -name '*.py' -print -exec tox -- {} --key $1 \;
fi