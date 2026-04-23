properties([
    pipelineTriggers([[$class: "SCMTrigger", scmpoll_spec: "H/15 * * * *"]])
])

node ("docker-light") {
    def SOURCEDIR = pwd()
    try {
        stage("Clean up") {
            step([$class: 'WsCleanup'])
        }
        stage("Checkout Code") {
            checkout scm
        }
        stage("Test with Docker") {
            echo "${env.ALT_URL}"
            def useUrl = ("${env.ALT_URL}" == "null") ? "${env.BINDING_TEST_URL}" : "${env.ALT_URL}"
            withEnv(["API_KEY=${env.ROSETTE_API_KEY}", "ALT_URL=${useUrl}"]) {
                sh "docker pull rosette/docker-python"
                sh "docker run --rm -e API_KEY=${API_KEY} -e ALT_URL=${ALT_URL} -v ${SOURCEDIR}:/source rosette/docker-python"
            }
        }
        slack(true)
    } catch (e) {
        currentBuild.result = "FAILED"
        postToTeams(false)
        throw e
    }
}

def postToTeams(boolean success) {
    def webhookUrl = "${env.TEAMS_PNC_JENKINS_WEBHOOK_URL}"
    def color = success ? "#00FF00" : "#FF0000"
    def status = success ? "SUCCESSFUL" : "FAILED"
    def message = "*" + status + ":* '${env.JOB_NAME}' - [${env.BUILD_NUMBER}] - ${env.BUILD_URL}"
    office365ConnectorSend(webhookUrl: webhookUrl, color: color, message: message, status: status)
}
