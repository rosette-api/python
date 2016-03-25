#!/bin/bash

#Gets called when the user doesn't provide any args
function HELP {
    echo -e "\nusage: source_file.py --key API_KEY [--url ALT_URL]"
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
        FILENAME)
            FILENAME=${OPTARG}
            usage
            ;;
        ALT_URL)
            ALT_URL=${OPTARG}
            usage
            ;;
    esac
done
ping_url="https://api.rosette.com/rest/v1"

# strip the trailing slash off of the alt_url if necessary
if [ ! -z "${ALT_URL}" ]; then
    case ${ALT_URL} in
        */) ALT_URL=${ALT_URL::-1}
            echo "Slash detected"
            ;;
    esac
    ping_url=${ALT_URL}
fi

#Checks for valid url
match=$(curl "${ping_url}/ping" -H "X-RosetteAPI-Key: ${API_KEY}" |  grep -o "Rosette API")
if [ "${match}" = "" ]; then
    echo -e "\n${ping_url} server not responding\n"
    exit 1
fi  

#Checks if Rosette API key is valid
function checkAPI {
    match=$(curl "${ping_url}/ping" -H "X-RosetteAPI-Key: ${API_KEY}" |  grep -o "forbidden")
    if [ ! -z $match ]; then
        echo -e "\nInvalid Rosette API Key"
        exit 1
    fi  
}

#Copy the examples from the mounted content in /source to current WORKDIR
cp  /source/examples/*.* .

#Run the examples
if [ ! -z ${API_KEY} ]; then
    checkAPI
    if [ ! -z ${FILENAME} ]; then
        if [ ! -z ${ALT_URL} ]; then
	    python ${FILENAME} --key ${API_KEY} --url ${ALT_URL} 
	else
	    python ${FILENAME} --key ${API_KEY} 
   	fi
    elif [ ! -z ${ALT_URL} ]; then
    	find -maxdepth 1  -name '*.py' -print -exec python {} --key ${API_KEY} --url ${ALT_URL} \;
    else
	find -maxdepth 1  -name '*.py' -print -exec python {} --key ${API_KEY} \;
    fi
else 
    HELP
fi
