@Library("eigi-jenkins-library") _
pipeline {
  agent { label "mockbuild" }
  environment {
    PKG_VER = sh(returnStdout: true, script: "date +%Y%m%d").trim()
    MOCK_CFG = "epel-7-x86_64-ul"
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
    stage("Collect data from RPM") {
      steps {
        script {
          env.BINARY_RPM = sh(returnStdout: true, script: "cd dist; ls *.noarch.rpm")
        }
      }
    }
    stage("Deploy to primemirror production repo") {
      steps {
        sh"sudo -u mirroradmin cp dist/*.noarch.rpm /var/www/html/mirrors/production/centos7/noarch/"
      }
    }
    stage("Sign RPM") {
      steps {
        script {
          try {
            String requestBody = common.v2.HttpsRequest.toJson([
              "elver": "7",
              "repo": "production",
              "arch": "noarch",
              "rpm": "${env.BINARY_RPM}" ])
              def request = new common.v2.HttpsRequest(this,
                "http://primemirror.unifiedlayer.com:8001/sign", "POST",
                ["contentType": "APPLICATION_JSON"], requestBody)
              def response = request.doHttpsRequest()
              if (response.getStatus() != 200) {
                echo response.getContent()
                error ("PrimeMirror API sign call failed.")
              }
              else {
                currentBuild.result = "SUCCESS";
              }
          }
          catch (Exception err) {
            currentBuild.result = "FAILURE";
          }
        }
      }
    }
    stage("Sync Production Repo to Mirrors Infrastructure") {
      steps {
        script {
          try {
            def request = new common.v2.HttpsRequest(this,
              "http://primemirror.unifiedlayer.com:8001/sync/production", "GET")
            def response = request.doHttpsRequest()
            currentBuild.result = "SUCCESS"
          } catch (Exception err) {
            currentBuild.result = "FAILURE"
          }
        }
      }
    }
    stage("Deploy") {
      steps {
        sh "echo DEPLOY"
        script {
          currentBuild.result = "SUCCESS"
        }
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
      sh "rm -rf ${WORKSPACE}/*"
    }
    success {
      echo "This ran because the pipeline was successful"
    }
    failure {
      echo "This ran because the pipeline failed"
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
