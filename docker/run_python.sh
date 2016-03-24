#!/bin/bash

retcode=0
ping_url="https://api.rosette.com/rest/v1"

#------------------ Functions ----------------------------------------------------
#Gets called when the user doesn't provide any args
function HELP {
    echo -e "\nusage: source_file.py --key API_KEY [--url ALT_URL]"
    echo "  API_KEY       - Rosette API key (required)"
    echo "  FILENAME      - Python source file (optional)"
    echo "  ALT_URL       - Alternate service URL (optional)"
    echo "  GIT_USERNAME  - Git username where you would like to push regenerated gh-pages (optional)"
    echo "  VERSION       - Build version (optional)"
    echo "Compiles and runs the source file(s) using the local development source."
    exit 1
}

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
    if [[ "${result}" == *"Exception"* ]]; then
        echo "Exception found"
        retcode=1
    elif [[ "$result" == *"processingFailure"* ]]; then
        retcode=1
    fi
}
#------------------ Functions End ------------------------------------------------

#Gets API_KEY, FILENAME and ALT_URL if present
while getopts ":API_KEY:FILENAME:ALT_URL:GIT_USERNAME:VERSION" arg; do
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
        GIT_USERNAME)
            GIT_USERNAME=${OPTARG}
            usage
            ;;
        VERSION)
            VERSION={OPTARG}
            usage
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
        runExample ${FILENAME}
    elif [ ! -z ${ALT_URL} ]; then
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

#Generate gh-pages and push them to git account (if git username is provided)
if [ ! -z ${GIT_USERNAME} ] && [ ! -z ${VERSION} ]; then
    #clone python git repo
    cd /
    git clone git@github.com:${GIT_USERNAME}/python.git
    cd python
    git checkout origin/gh-pages -b gh-pages
    git branch -d develop
    #generate gh-pages and set ouput dir to git repo (gh-pages branch)
    cd /python-dev
    .tox/py27/bin/epydoc -v --no-private --no-frames --css epydoc.css -o /python rosette/*.py
    cd /python
    git add .
    git commit -a -m "publish python apidocs ${VERSION}"
    git push
fi

exit ${retcode}
