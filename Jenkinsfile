@Library('eigi-jenkins-library') _
pipeline {
  agent { label "mockbuild" }
  environment {
    RELEASE_STR = "${params.release == "" ? "1" : params.release}"
    PKG_VER = sh(returnStdout: true, script: "date +%Y%m%d").trim()
    MOCK_CFG = "epel-${params.elvers}-x86_64-ul"
    TAR_FILE = "sources/${pkgName}-${PKG_VER}.tar.bz2"
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
             env.BINARY_RPM = sh(returnStdout: true, script: "ls ${workspace}/dist/*.noarch.rpm"
          }
      }
    }
    stage("Deploy to primemirror web root") {
        steps {
            sh "sudo -u mirroradmin cp ${WORKSPACE}/dist/${env.BINARY_RPM} /var/www/html/mirrors/production/centos7/noarch/"
        }
    }
    stage("Sign RPM with production key") {
        steps {
	    sh "echo Sign RPM"
	    script {
		Map requestProperties = ['acceptType':'APPLICATION_JSON']
		String requestBody '"repo": "production", "rpm": "", "elver": 7, "arch": "noarch"'
                String url "http://primemirror.unifiedlayer.com:8001/sign"
		def request = new HttpsRequest(this, url, "POST", requestProperties, requestBody)
    		def response = request.doHttpsRequest()
    		if (response.getStatus() == 200) {
        	    echo response.getContent()
    		}
            }
        }
    }
    stage("Update alpha yum repo metadata") {
        steps {
            sh "sudo -i -u mirroradmin createrepo --update /var/www/html/mirrors/production/centos7"
        }
    }
    stage("Sync Repo to Mirrors Infrastructure") {
        steps {
            sh "sudo -u mirroradmin /home/mirroradmin/repo_sync.py --repo production"
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
