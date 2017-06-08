#!/usr/bin/env groovy

pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                sh 'python3 managy.py db init'
                sh 'python3 managy.py db migrate -m "initial migration"'
                sh 'python3 managy.py db upgrade'
            }
        }

        stage('Test') {
            steps {
                echo 'No test available!'
            }
        }

        stage('Deploy') {
            steps {
                sh 'pm2 startOrRestart ecosystem.config.js --env dev'
            }
        }
    }
}