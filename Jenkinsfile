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

        stage('Static Code Checks') {
            steps {
                sh 'pipenv check'
                sh 'pipenv run black setup.py dclient/* tests/*'
                sh 'pipenv run flake8'
            }
        }
    }
}
