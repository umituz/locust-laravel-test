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
                sh 'docker-compose -f docker-compose.yml up -d'
                sh 'docker-compose -f docker-compose.yml exec -T laravel.test php artisan test'
            }
        }

        stage('Run Locust Tests') {
            steps {
                sh '''
                docker run --rm --network nebuchadnezzar_network \
                    -v ${WORKSPACE}:/mnt/locust \
                    locustio/locust \
                    -f /mnt/locust/tests/locust/locustfile.py \
                    --host=http://laravel.test \
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
            sh 'docker-compose -f docker-compose.yml down'
            archiveArtifacts artifacts: 'locust*.csv', allowEmptyArchive: true
        }
    }
}
