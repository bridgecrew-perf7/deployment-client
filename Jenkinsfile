pipeline {
    agent {
        label 'primemirror'
    }
    stages {
        stage('Setup Virtualenv') {
            steps {
                sh 'pipenv --rm'
                sh 'pipenv install --dev'
            }
        }

        stage('Code Checks') {
            steps {
                sh 'pipenv check'
                sh 'pipenv run black *.py'
                sh 'pipenv run flake8'
            }
        }
    }
}
