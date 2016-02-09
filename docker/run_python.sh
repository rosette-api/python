#!/bin/bash

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

#Checks if Rosette API key is valid
function checkAPI {
    match=$(curl "https://api.rosette.com/rest/v1/ping" -H "user_key: ${API_KEY}" |  grep -o "forbidden")
    if [ ! -z $match ]; then
        echo -e "\nInvalid Rosette API Key"
        exit 1
    fi  
}

#Copy the mounted content in /source to current WORKDIR
cp -r -n /source/* .

#Run the examples
if [ ! -z ${API_KEY} ]; then
    checkAPI
    #Prerequisite
    python /python-dev/setup.py install
    cd /python-dev/examples
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

#Run unit tests
cd /python-dev
tox

#Generate gh-pages and push them to git account (if git username is provided)
if [ ! -z ${GIT_USERNAME} ] && [ ! -z ${VERSION} ]; then
    #clone git repo
    cd /
    git clone https://github.com/${GIT_USERNAME}/python.git
    cd python
    git checkout origin/gh-pages -b gh-pages
    git branch -d develop
     #generate gh-pages and set ouput dir to git repo (gh-pages branch)
    cd /python-dev
    .tox/py27/bin/epydoc -v --no-private --no-frames --css epydoc.css -o /python rosette/*.py
    cd /python
    git add .
    git config --global user.email "${GIT_USERNAME}"
    git config --global user.name "${GIT_USERNAME}"
    git commit -a -m "publish python apidocs ${VERSION}"
    git push
fi