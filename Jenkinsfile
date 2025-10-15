pipeline {
    agent any

    environment {
        BASE_URL = 'http://dev.bootcamp.store.supersqa.com'
        BROWSER = 'chrome'

        WOO_KEY = credentials('WOO_KEY')
        WOO_SECRET = credentials('WOO_SECRET')
        DB_USER = credentials('DB_USER')
        DB_PASSWORD = credentials('DB_PASSWORD')
    }

    stages {
        stage('Checkout') {
            steps {
                git credentialsId: 'github repo access 1', url: 'https://github.com/milenagrabovskiy/Ecommerce-Pytest-Framework.git'
            }
        }

        stage('Setup Python Environment') {
            steps {
                sh '''
                    python3 -m venv my_venv
                    . my_venv/bin/activate
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Smoke Tests') {
            parallel {
                stage('Backend Smoke') {
                    steps {
                        sh '''
                            . my_venv/bin/activate
                            export PYTHONPATH=$WORKSPACE
                            cd demostore_automation
                            python3 -m pytest tests/backend/ -m smoke --junitxml=$WORKSPACE/output/backend_smoke.xml || true
                        '''
                    }
                    post { always { junit 'output/backend_smoke.xml' } }
                }

                stage('Frontend Smoke Chrome') {
                    steps {
                        sh '''
                            . my_venv/bin/activate
                            export PYTHONPATH=$WORKSPACE
                            export BROWSER=headlesschrome
                            cd demostore_automation
                            python3 -m pytest tests/frontend/ -m smoke --junitxml=$WORKSPACE/output/frontend_smoke_chrome.xml || true
                        '''
                    }
                    post { always { junit 'output/frontend_smoke_chrome.xml' } }
                }

                stage('Frontend Smoke Firefox') {
                    steps {
                        sh '''
                            . my_venv/bin/activate
                            export PYTHONPATH=$WORKSPACE
                            export BROWSER=headlessfirefox
                            cd demostore_automation
                            python3 -m pytest tests/frontend/ -m smoke --junitxml=$WORKSPACE/output/frontend_smoke_firefox.xml || true
                        '''
                    }
                    post { always { junit 'output/frontend_smoke_firefox.xml' } }
                }
            }
        }

        stage('Regression Tests') {
            parallel {
                stage('Backend Regression') {
                    steps {
                        sh '''
                            . my_venv/bin/activate
                            export PYTHONPATH=$WORKSPACE
                            cd demostore_automation
                            python3 -m pytest tests/backend/ --junitxml=$WORKSPACE/output/backend_regression.xml || true
                        '''
                    }
                    post { always { junit 'output/backend_regression.xml' } }
                }

                stage('Frontend Regression Chrome') {
                    steps {
                        sh '''
                            . my_venv/bin/activate
                            export PYTHONPATH=$WORKSPACE
                            export BROWSER=headlesschrome
                            cd demostore_automation
                            python3 -m pytest tests/frontend/ --junitxml=$WORKSPACE/output/frontend_regression_chrome.xml || true
                        '''
                    }
                    post { always { junit 'output/frontend_regression_chrome.xml' } }
                }

                stage('Frontend Regression Firefox') {
                    steps {
                        sh '''
                            . my_venv/bin/activate
                            export PYTHONPATH=$WORKSPACE
                            export BROWSER=headlessfirefox
                            cd demostore_automation
                            python3 -m pytest tests/frontend/ --junitxml=$WORKSPACE/output/frontend_regression_firefox.xml || true
                        '''
                    }
                    post { always { junit 'output/frontend_regression_firefox.xml' } }
                }
            }
        }
    }
}
