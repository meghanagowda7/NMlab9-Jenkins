pipeline {
    agent {
        docker {
            image 'node'
            args '-u root'
        }
    }
    stages {
        stage('Package Update/Install') {
            steps {
                echo 'Updating/Installing necessary packages...........'
                sh 'apt-get update'
                sh 'apt-get upgrade -y'
                sh 'apt-get install -y python3-pip'
                sh 'python3 -m pip install ncclient'
            }
        }
        stage('Violation Check') { 
            steps {
                echo 'Checking script violations.............'
                sh 'python3 -m pip install pylint'
                sh 'pylint static_yang_config.py --fail-under=5'
                }
            }
        stage('Application Run') { 
            steps {
                echo 'Running application....' 
                sh 'python3 static_yang_config.py'
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
