

def versions = [3.7, 3.8, 3.9, 3.10, 3.11]

def runSonnarForPythonVersion(sourceDir, ver){
    mySonarOpts="-Dsonar.sources=/source -Dsonar.host.url=${env.SONAR_HOST_URL} -Dsonar.login=${env.SONAR_AUTH_TOKEN}"
    if("${env.CHANGE_ID}" != "null"){
        mySonarOpts = "$mySonarOpts -Dsonar.pullrequest.key=${env.CHANGE_ID} -Dsonar.pullrequest.branch=${env.BRANCH_NAME}"
    } else {
        mySonarOpts = "$mySonarOpts -Dsonar.branch.name=${env.BRANCH_NAME}"
    } 
    if ("${env.CHANGE_BRANCH}" != "null") {
        mySonarOpts="$mySonarOpts -Dsonar.pullrequest.base=${env.CHANGE_TARGET} -Dsonar.pullrequest.branch=${env.CHANGE_BRANCH}"
    }

    // Only run Sonar once.
    if(ver == 3.11) {
        sonarExec="cd /root/ && \
                   wget -q https://github.com/SonarSource/sonar-scanner-cli/archive/refs/tags/4.8.1.3023.zip && \
                   unzip -q 4.8.1.3023.zip && \
                   cd /source && \
                   /root/sonar-scanner-4.8.1.3023/bin/sonar-scanner ${mySonarOpts}"
    } else {
        sonarExec="echo Skipping Sonar for this version."
    }

    sh "docker run \
            --pull always \
            --rm --volume ${sourceDir}:/source \
            python:${ver}-slim \
            bash -c \"apt-get update && \
            apt-get install -y wget unzip && \
            pip3 install tox && \
            cd /source && \
            tox && \
            ${sonarExec}\""
}

node ("docker-light") {
    def sourceDir = pwd()
    try {
        stage("Clean up") {
            step([$class: 'WsCleanup'])
        }
        stage("Checkout Code") {
            checkout scm
        }
        stage("Build & Test") {
            withSonarQubeEnv {
                
                versions.each { ver ->
                    runSonnarForPythonVersion(sourceDir, ver)
                }
            }
        }
    } catch (e) {
        currentBuild.result = "FAILED"
        throw e
    }
}
