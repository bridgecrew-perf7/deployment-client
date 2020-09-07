@Library('eigi-jenkins-library') _
pipeline {
  agent { label "mockbuild" }
  environment {
    RELEASE_STR = "${params.release == "" ? "1" : params.release}"
    PKG_VER = sh(returnStdout: true, script: "date +%Y%m%d").trim()
    MOCK_CFG = "epel-${params.elvers}-x86_64-ul"
    EXCLUDE_FILE = sh(
                        script:
                          """
                            if [ -f rpm/excludes.txt ]
                            then
                              echo "rpm/excludes.txt"
                            fi
                          """,
                        returnStdout: true).trim()
  }
  stages {
    stage("Prepare") {
      steps {
        sh "echo PREPARE"
      }
    }
    stage("Test") {
      steps {
        sh "echo TEST"
      }
    }
    stage("Create RPM") {
      steps {
        sh"python setup.py bdist_rpm"
      }
    }
    stage('Collect data from RPM') {
      steps {
        script {
          env.BINARY_RPM = sh(returnStdout: true, script: "cd ${WORKSPACE}/dist; ls *.noarch.rpm")
          env.REPO = "/var/www/html/mirrors/production/centos7/noarch/"
        }
      }
    }
    stage("Deploy to primemirror production repo") {
      steps {
        sh """
	     sudo -u mirroradmin cp dist/${env.BINARY_RPM} ${env.REPO}
	   """
      }
    }
    stage('Sign RPM') {
      steps {
        script {
          String requestBody = common.v2.HttpsRequest.toJson([
            'elver':    7, 
            'repo':     "production",
            'arch':     "noarch", 
            'rpm' :     "${env.BINARY_RPM}"])
          def request = new common.v2.HttpsRequest(this,
            'http://primemirror.unifiedlayer.com:8001/sign', "POST",
            [:], requestBody)
          def response = request.doHttpsRequest()
            if (response.getStatus() != 200) {
              echo response.getContent()
              error ('PrimeMirror API call failed.')
            }
         }
      }
    }
    stage('Sync Production Repo to Mirrors Infrastructure') {
      steps {
        script {
          def request = new common.v2.HttpsRequest(this,
            'http://primemirror.unifiedlayer.com:8001/sync/production', "GET")
          def response = request.doHttpsRequest()
            if (response.getStatus() != 200) {
              echo response.getContent()
              error ('PrimeMirror API call failed.')
            }
         }
      }
    }
    stage("Deploy") {
      steps {
        sh "echo DEPLOY"
      }
    }
  }
  post {
    always {
      echo "This will always run"
      script {
        echo "Pipeline result: ${currentBuild.result}"
        echo "Pipeline currentResult: ${currentBuild.currentResult}"
        notifyBitbucket()
      }
    }
    success {
      echo "This ran because the pipeline was successful"
      sh "rm -rf ${WORKSPACE}"
    }
    failure {
      echo "This ran because the pipeline failed"
      sh "rm -rf ${WORKSPACE}"
    }
    unstable {
      echo "This ran because the pipeline was marked unstable"
    }
    changed {
      echo "This ran because the state of the Pipeline has changed"
      echo "For example, if the Pipeline was previously failing but is now successful"
    }
  }
}
