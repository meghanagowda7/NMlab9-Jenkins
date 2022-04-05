pipeline {
    agent any

    stages {
        stage('Update/Install packages in Netman VM') { 
            steps {
                sh 'sudo apt-get install -y python-ncclient'
                sh 'sudo apt install python3-pandas'
                sh 'sudo apt-get install python-ipaddress'
                sh 'sudo apt-get install python-prettytable'
            }
        }
        stage('Checking and fixing violations') { 
            steps {
                sh 'sudo apt install python3-pip python3-dev'
                sh 'pip3 install pylint'
                sh 'pylint netman_netconf_obj2.py'
            }
        }
         stage('Running the application') {
            steps {
                sh 'python3 netman_netconf_obj2.py'
            }
        }
         stage('Unit Test') { 
            steps {
                echo 'Unit Test!'
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
