node {
    def SOURCEDIR = pwd()
    try {
        stage("Clean up") {
            step([$class: 'WsCleanup'])
        }
        stage("Checkout Code") {
            checkout scm
        }
        stage("Test with Docker") {
            withEnv(["API_KEY=${env.ROSETTE_API_KEY}", "ALT_URL=${env.BINDING_TEST_URL}"]) {
                sh "docker pull rosetteapi/docker-python"
                sh "docker run --rm -e API_KEY=${API_KEY} -e ALT_URL=${ALT_URL} -v ${SOURCEDIR}:/source rosetteapi/docker-python"
            }
        }
        slack(true)
    } catch (e) {
        currentBuild.result = "FAILED"
        slack(false)
        throw e
    }
}

def slack(boolean success) {
    def color = success ? "#00FF00" : "#FF0000"
    def status = success ? "SUCCESSFUL" : "FAILED"
    def message = status + ": Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]' (${env.BUILD_URL})"
    slackSend(color: color, channel: "#rapid", message: message)
}