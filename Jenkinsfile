pipeline {
    agent {
        docker {
            image 'node'
            args '-u root'
        }
    }
    stages {
        stage('Testing') {
            steps {
                sh 'apt-get update'
                sh 'apt-get upgrade -y'
                sh 'apt-get install -y python3-pip'
                sh 'python3 -m pip install napalm'
                sh 'python3 test.py'
            }
        }
    }
    post
    {
        success
        {
            emailext body: 'Build Successful, happy coding :)', subject: 'Build pipeline status', to: 'meghana.gowda@colorado.edu'
        }
        failure
        {
            emailext body: 'Build Failed, check code and try again', subject: 'Build pipeline status', to: 'meghana.gowda@colorado.edu'
        }
    }
}
