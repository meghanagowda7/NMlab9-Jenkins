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
                echo 'Checking and fixing violations!'
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
}
