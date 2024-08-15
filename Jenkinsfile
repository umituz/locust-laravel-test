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
                sh 'docker-compose -f /path/to/laravel/docker-compose.yml exec -T laravel.test php artisan test'
            }
        }

        stage('Run Locust Tests') {
            steps {
                sh """
                docker-compose -f /path/to/locust/docker-compose.yml run --rm locust-master \
                    locust -f /mnt/locust/locustfiles/ferris/locustfile.py \
                    --host=http://laravel.test --headless -u 20 -r 2 --run-time 5m
                """
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'locust*.csv', fingerprint: true
        }
    }
}
