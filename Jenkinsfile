pipeline {
    agent any

    environment {
        DB_PORT = '3308'
        DB_HOST = 'dev.bootcamp.store.supersqa.com'
        DB_DATABASE = 'demostore'
        DB_TABLE_PREFIX = 'wp_'
        BASE_URL = 'http://dev.bootcamp.store.supersqa.com'
        BROWSER = 'chrome'

        WOO_KEY = credentials('WOO_KEY')
        WOO_SECRET = credentials('WOO_SECRET')
        DB_USER = credentials('DB_USER')
        DB_PASSWORD = credentials('DB_PASSWORD')
    }

    stages {

        stage('Setup Python Environment') {
            steps {
                sh '''
                    python3 -m venv my_venv
                    . my_venv/bin/activate
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run All Tests in Parallel') {
            parallel {

                'Backend Smoke': {
                    steps {
                        catchError(buildResult: 'UNSTABLE', stageResult: 'UNSTABLE') {
                            sh '''
                                . my_venv/bin/activate
                                set -a
                                source variables_local.env
                                set +a
                                export PYTHONPATH=$WORKSPACE
                                cd demostore_automation/tests/backend
                                python3 -m pytest -m smoke --junitxml=$WORKSPACE/output/backend_smoke.xml -v
                            '''
                        }
                    }
                    post { always { junit 'output/backend_smoke.xml' } }
                }

                'Backend Regression': {
                    steps {
                        catchError(buildResult: 'UNSTABLE', stageResult: 'UNSTABLE') {
                            sh '''
                                . my_venv/bin/activate
                                . ./variables_local.env
                                export PYTHONPATH=$WORKSPACE
                                cd demostore_automation
                                python3 -m pytest tests/backend/ --junitxml=$WORKSPACE/output/backend_regression.xml
                            '''
                        }
                    }
                    post { always { junit 'output/backend_regression.xml' } }
                }

                'Frontend Smoke Firefox': {
                    steps {
                        catchError(buildResult: 'UNSTABLE', stageResult: 'UNSTABLE') {
                            sh '''
                                . my_venv/bin/activate
                                . ./variables_local.env
                                export PYTHONPATH=$WORKSPACE
                                export BROWSER=headlessfirefox
                                cd demostore_automation
                                python3 -m pytest tests/frontend/ -m smoke --junitxml=$WORKSPACE/output/frontend_smoke_firefox.xml
                            '''
                        }
                    }
                    post { always { junit 'output/frontend_smoke_firefox.xml' } }
                }

                'Frontend Smoke Chrome': {
                    steps {
                        catchError(buildResult: 'UNSTABLE', stageResult: 'UNSTABLE') {
                            sh '''
                                . my_venv/bin/activate
                                . ./variables_local.env
                                export PYTHONPATH=$WORKSPACE
                                export BROWSER=headlesschrome
                                cd demostore_automation
                                python3 -m pytest tests/frontend/ -m smoke --junitxml=$WORKSPACE/output/frontend_smoke_chrome.xml
                            '''
                        }
                    }
                    post { always { junit 'output/frontend_smoke_chrome.xml' } }
                }

                'Frontend Regression Firefox': {
                    steps {
                        catchError(buildResult: 'UNSTABLE', stageResult: 'UNSTABLE') {
                            sh '''
                                . my_venv/bin/activate
                                . ./variables_local.env
                                export PYTHONPATH=$WORKSPACE
                                export BROWSER=headlessfirefox
                                cd demostore_automation
                                python3 -m pytest tests/frontend/ --junitxml=$WORKSPACE/output/frontend_regression_firefox.xml
                            '''
                        }
                    }
                    post { always { junit 'output/frontend_regression_firefox.xml' } }
                }

                'Frontend Regression Chrome': {
                    steps {
                        catchError(buildResult: 'UNSTABLE', stageResult: 'UNSTABLE') {
                            sh '''
                                . my_venv/bin/activate
                                . ./variables_local.env
                                export PYTHONPATH=$WORKSPACE
                                export BROWSER=headlesschrome
                                cd demostore_automation
                                python3 -m pytest tests/frontend/ --junitxml=$WORKSPACE/output/frontend_regression_chrome.xml
                            '''
                        }
                    }
                    post { always { junit 'output/frontend_regression_chrome.xml' } }
                }
            }
        }
    }
}
