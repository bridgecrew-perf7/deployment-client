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
                sh 'find . -name "*.py" -print0 | xargs -0 -I "{}" pipenv run black "{}"'
                sh 'pipenv run flake8 --ignore E501'
            }
        }
    }
}
