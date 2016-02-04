#!/bin/bash

#Gets called when the user doesn't provide any args
function HELP {
	echo "usage: source_file.py --key API_KEY [--url ALT_URL]"
    echo "  API_KEY      - Rosette API key (required)"
    echo "  FILENAME     - Python source file (optional)"
    echo "  ALT_URL      - Alternate service URL (optional)"
    echo "Compiles and runs the source file(s) using the published rosette-api"
    exit 1
}

#Gets API_KEY, FILENAME and ALT_URL if present
while getopts ":API_KEY:FILENAME:ALT_URL" arg; do
    case "${arg}" in
        API_KEY)
            API_KEY=${OPTARG}
            usage
            ;;
        ALT_URL)
            ALT_URL=${OPTARG}
            usage
            ;;
        FILENAME)
            FILENAME=${OPTARG}
            usage
            ;;
    esac
done

# reference the API 
curl "https://api.rosette.com/rest/v1/ping" -H "user_key: $1"

#Copy the mounted content in /source to current WORKDIR
cp /source/*.* .

#Run the examples
if [ ! -z ${API_KEY} ]; then
	if [ ! -z ${FILENAME} ]; then
		if [ ! -z ${ALT_URL} ]; then
			tox -- ${FILENAME} --key ${API_KEY} --url ${ALT_URL} 
		else
			tox -- ${FILENAME} --key ${API_KEY} 
   		fi
	elif [ ! -z ${ALT_URL} ]; then
    	find -maxdepth 1  -name '*.py' -print -exec tox -- {} --key ${API_KEY} --url ${ALT_URL} \;
	else
		find -maxdepth 1  -name '*.py' -print -exec tox -- {} --key ${API_KEY} \;
    fi
else 
	HELP
fi