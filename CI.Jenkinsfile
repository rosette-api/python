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
                        echo \"------about to build------\" && \
                        cd /source && \
                        tox && \
                        echo \"------finish setup------\" && \
                        /root/sonar-scanner-4.8.0.2856-linux/bin/sonar-scanner \
                        -Dsonar.sources=/source \
                        -Dsonar.host.url=${env.SONAR_HOST_URL} \
                        -Dsonar.login=${env.SONAR_AUTH_TOKEN}\""
            }
        }
    } catch (e) {
        currentBuild.result = "FAILED"
        throw e
    }
}