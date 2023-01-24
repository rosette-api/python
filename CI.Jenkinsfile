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
                sh "docker run -it --env PATH=\"/root/sonar-scanner/bin:${PATH}\" --volume /Users/yaison/work/basis/git/rosette-api/python/rosette:/source python:3.6-slim bash -c \"apt-get update && \
                        apt-get install -y python3-pip && \
                        apt-get install -y wget unzip && \
                        cd / && \
                        wget https://download.java.net/java/GA/jdk19.0.2/fdb695a9d9064ad6b064dc6df578380c/7/GPL/openjdk-19.0.2_linux-x64_bin.tar.gz && \
                        tar -xvf openjdk-19.0.2_linux-x64_bin.tar.gz && \
                        export JAVA_HOME=/jdk-19.0.2 && \
                        export PATH=\"/jdk-19.0.2/bin:$PATH\" && \
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