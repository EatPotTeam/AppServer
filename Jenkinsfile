#!/usr/bin/env groovy

pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                sh './ci/build.sh'
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