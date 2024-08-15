pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                // Laravel projesini klonla
                git 'https://github.com/umituz/locust-laravel-test.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                // Composer bağımlılıklarını yükle
                sh 'composer install'
            }
        }

        stage('Build and Test') {
            steps {
                // Docker grubuna geçici olarak ekle
                sh 'sudo usermod -aG docker jenkins'
                // Docker daemon'ı yeniden başlat
                sh 'sudo systemctl restart docker'
                // Sail'i çalıştır
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
            sh './vendor/bin/sail down'
            archiveArtifacts artifacts: 'locust*.csv', allowEmptyArchive: true
            // Jenkins kullanıcısını Docker grubundan çıkar
            sh 'sudo gpasswd -d jenkins docker'
        }
    }
}
