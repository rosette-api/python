#!/bin/bash

retcode=0
ping_url="https://api.rosette.com/rest/v1"
errors=( "Exception" "processingFailure" "badRequest" "ParseError" "ValueError" "SyntaxError" "AttributeError" "ImportError" )

#------------------ Functions ----------------------------------------------------
#Gets called when the user doesn't provide any args
function HELP {
    echo -e "\nusage: --key API_KEY [--FILENAME filename] [--url ALT_URL]"
    echo "  API_KEY       - Rosette API key (required)"
    echo "  FILENAME      - Python source file (optional)"
    echo "  ALT_URL       - Alternate service URL (optional)"
    echo "Compiles and runs the source file(s) using the local development source."
    exit 1
}

if [ ! -z ${ALT_URL} ]; then
    ping_url=${ALT_URL}
fi

#Checks if Rosette API key is valid
function checkAPI {
    match=$(curl "${ping_url}/ping" -H "X-RosetteAPI-Key: ${API_KEY}" |  grep -o "forbidden")
    if [ ! -z $match ]; then
        echo -e "\nInvalid Rosette API Key"
        exit 1
    fi  
}

function cleanURL() {
    # strip the trailing slash off of the alt_url if necessary
    if [ ! -z "${ALT_URL}" ]; then
        case ${ALT_URL} in
            */) ALT_URL=${ALT_URL::-1}
                echo "Slash detected"
                ;;
        esac
        ping_url=${ALT_URL}
    fi
}

function validateURL() {
    match=$(curl "${ping_url}/ping" -H "X-RosetteAPI-Key: ${API_KEY}" |  grep -o "Rosette API")
    if [ "${match}" = "" ]; then
        echo -e "\n${ping_url} server not responding\n"
        exit 1
    fi  
}

function runExample() {
    echo -e "\n---------- ${1} start -------------"
    result=""
    if [ -z ${ALT_URL} ]; then
        result="$(python ${1} --key ${API_KEY} 2>&1 )"
    else
        result="$(python ${1} --key ${API_KEY} --url ${ALT_URL} 2>&1 )"
    fi
    echo "${result}"
    echo -e "\n---------- ${1} end -------------"
    for err in "${errors[@]}"; do 
        if [[ ${result} == *"${err}"* ]]; then
            retcode=1
        fi
    done
}
#------------------ Functions End ------------------------------------------------

#Gets API_KEY, FILENAME and ALT_URL if present
while getopts ":API_KEY:FILENAME:ALT_URL" arg; do
    case "${arg}" in
        API_KEY)
            API_KEY=${OPTARG}
            ;;
        ALT_URL)
            ALT_URL=${OPTARG}
            ;;
        FILENAME)
            FILENAME=${OPTARG}
            ;;
    esac
done

cleanURL

validateURL


#Copy the mounted content in /source to current WORKDIR
cp -r -n /source/* .

#Run the examples
if [ ! -z ${API_KEY} ]; then
    checkAPI
    #Prerequisite
    python /python-dev/setup.py install
    cd /python-dev/examples
    if [ ! -z ${FILENAME} ]; then
        echo -e "\nRunning example against: ${ping_url}\n"
        runExample ${FILENAME}
    else
        echo -e "\nRunning examples against: ${ping_url}\n"
        for file in *.py; do
            runExample ${file}
        done
    fi
else 
    HELP
fi

#Run unit tests
cd /python-dev
tox

exit ${retcode}
