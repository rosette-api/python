

def versions = [3.11, 3.10, 3.9, 3.8, 3.7]

def runSonnarForPythonVersion(sourceDir, ver){
    mySonarOpts="-Dsonar.sources=/source -Dsonar.pullrequest.branch=${env.BRANCH_NAME} -Dsonar.host.url=${env.SONAR_HOST_URL} -Dsonar.login=${env.SONAR_AUTH_TOKEN}"
    if ("${env.CHANGE_BRANCH}" != "null") {
        mySonarOpts="$mySonarOpts -Dsonar.pullrequest.key=${env.CHANGE_ID} -Dsonar.pullrequest.base=${env.CHANGE_TARGET} -Dsonar.pullrequest.branch=${env.CHANGE_BRANCH}"
    }else{
        mySonarOpts="$mySonarOpts -Dsonar.pullrequest.branch=${env.BRANCH_NAME}"
    }
    sh "docker run \
            --pull always \
            --rm --volume ${sourceDir}:/source \
            python:${ver}-slim \
            bash -c \"apt-get update && \
            apt-get install -y wget unzip && \
            pip3 install tox && \
            cd /root/ && \
            wget https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-4.8.0.2856-linux.zip && \
            unzip sonar-scanner-cli-4.8.0.2856-linux.zip && \
            cd /source && \
            tox && \
            /root/sonar-scanner-4.8.0.2856-linux/bin/sonar-scanner \
            ${mySonarOpts}\""
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