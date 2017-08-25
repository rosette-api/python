node {
    environment {
        SOURCEDIR = pwd()
    }
    try {
        stage("Clean up") {
            step([$class: 'WsCleanup'])
        }
        stage("Checkout Code") {
            checkout scm
            echo ${sourceDir}
        }
        stage("Test with Docker") {
            withEnv(["API_KEY=env.ROSETTE_API_KEY"]) {
                docker.image('rosetteapi/docker-python').run([
                    "-e API_KEY=${API_KEY}",
                    "-v ${SOURCEDIR}:/source"
                ])
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