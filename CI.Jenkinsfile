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
                sh "docker run -it --env PATH=\"/root/sonar-scanner/bin:${PATH}\" --volume ${sourceDir}:/source python:3.6-slim bash -c \"apt-get update && \
                        apt-get install -y python3-pip && \
                        apt-get install -y wget unzip && \
                        pip3 install tox && \
                        cd /root/ && \
                        wget https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-4.8.0.2856-linux.zip && \
                        unzip sonar-scanner-cli-4.8.0.2856-linux.zip && \
                        rm sonar-scanner-cli-4.8.0.2856-linux.zip && \
                        ln -s sonar-scanner-4.8.0.2856/ sonar-scanner && \
                        apt-get purge -y --auto-remove unzip && \
                        rm -rf /var/lib/apt/lists/* && \
                        echo \"------finish setup------\" && \
                        /root/sonar-scanner-4.8.0.2856-linux/bin/sonar-scanner \
                        -Dsonar.sources=/source \
                        -Dsonar.host.url=${sonar_host} \
                        -Dsonar.login=${sonar_token}\""
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
    slackSend(color: color, channel: "#p-n-c_jenkins", message: message)
}