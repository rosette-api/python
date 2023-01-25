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
                sh "docker run \
                      --pull always \
                      --rm --volume ${sourceDir}:/source \
                      python:3.6-slim \
                      bash -c \"pip3 install tox && \
                        cd /source && \
                        tox\""
            }
        }
    } catch (e) {
        currentBuild.result = "FAILED"
        throw e
    }
}