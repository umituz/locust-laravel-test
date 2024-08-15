pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build and Test') {
            steps {
                sh './vendor/bin/sail up -d'
                sh './vendor/bin/sail artisan test'
            }
        }

        stage('Run Locust Tests') {
            steps {
                sh '''
                ./vendor/bin/sail exec -T laravel.test pip install locust
                ./vendor/bin/sail exec -T laravel.test locust \
                    -f tests/locust/locustfile.py \
                    --host=http://localhost \
                    --users 10 \
                    --spawn-rate 1 \
                    --run-time 1m \
                    --headless \
                    --only-summary
                '''
            }
        }
    }

    post {
        always {
            sh './vendor/bin/sail down'
            archiveArtifacts artifacts: 'locust*.csv', allowEmptyArchive: true
        }
    }
}
