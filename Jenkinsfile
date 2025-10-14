pipeline {
    agent any

    environment {
        DB_PORT         = '3308'
        DB_HOST         = 'dev.bootcamp.store.supersqa.com'
        DB_DATABASE     = 'demostore'
        DB_TABLE_PREFIX = 'wp_'
        BASE_URL        = 'http://dev.bootcamp.store.supersqa.com'
        BROWSER         = 'chrome'

        WOO_KEY         = credentials('WOO_KEY')
        WOO_SECRET      = credentials('WOO_SECRET')
        DB_USER         = credentials('DB_USER')
        DB_PASSWORD     = credentials('DB_PASSWORD')
    }

    stages {

        // -------------------
        // Setup Python Environment
        // -------------------
        stage('Setup Python Environment') {
            steps {
                sh '''#!/bin/bash
                    set -xe
                    python3 -m venv my_venv
                    source my_venv/bin/activate
                    pip install -r requirements.txt
                '''
            }
        }

        // -------------------
        // Backend Smoke Tests
        // -------------------
        stage('Backend Smoke Tests') {
            steps {
                catchError(buildResult: 'UNSTABLE', stageResult: 'UNSTABLE') {
                    sh '''#!/bin/bash
                        set -xe
                        source my_venv/bin/activate
                        export PYTHONPATH=$WORKSPACE
                        cd demostore_automation
                        pytest tests/backend/ -m smoke --junitxml=$WORKSPACE/output/backend_smoke.xml || true
                    '''
                }
            }
            post { always { junit 'output/backend_smoke.xml' } }
        }

        // -------------------
        // Backend Regression Tests
        // -------------------
        stage('Backend Regression Tests') {
            steps {
                catchError(buildResult: 'UNSTABLE', stageResult: 'UNSTABLE') {
                    sh '''#!/bin/bash
                        set -xe
                        source my_venv/bin/activate
                        export PYTHONPATH=$WORKSPACE
                        cd demostore_automation
                        pytest tests/backend/ --junitxml=$WORKSPACE/output/backend_regression.xml || true
                    '''
                }
            }
            post { always { junit 'output/backend_regression.xml' } }
        }

        // -------------------
        // Frontend Smoke Firefox
        // -------------------
        stage('Frontend Smoke Firefox') {
            steps {
                catchError(buildResult: 'UNSTABLE', stageResult: 'UNSTABLE') {
                    sh '''#!/bin/bash
                        set -xe
                        source my_venv/bin/activate
                        export PYTHONPATH=$WORKSPACE
                        export BROWSER=headlessfirefox
                        cd demostore_automation
                        pytest tests/frontend/ -m smoke --junitxml=$WORKSPACE/output/frontend_smoke_firefox.xml || true
                    '''
                }
            }
            post { always { junit 'output/frontend_smoke_firefox.xml' } }
        }

        // -------------------
        // Frontend Smoke Chrome
        // -------------------
        stage('Frontend Smoke Chrome') {
            steps {
                catchError(buildResult: 'UNSTABLE', stageResult: 'UNSTABLE') {
                    sh '''#!/bin/bash
                        set -xe
                        source my_venv/bin/activate
                        export PYTHONPATH=$WORKSPACE
                        export BROWSER=headlesschrome
                        cd demostore_automation
                        pytest tests/frontend/ -m smoke --junitxml=$WORKSPACE/output/frontend_smoke_chrome.xml || true
                    '''
                }
            }
            post { always { junit 'output/frontend_smoke_chrome.xml' } }
        }

        // -------------------
        // Frontend Regression Firefox
        // -------------------
        stage('Frontend Regression Firefox') {
            steps {
                catchError(buildResult: 'UNSTABLE', stageResult: 'UNSTABLE') {
                    sh '''#!/bin/bash
                        set -xe
                        source my_venv/bin/activate
                        export PYTHONPATH=$WORKSPACE
                        export BROWSER=headlessfirefox
                        cd demostore_automation
                        pytest tests/frontend/ --junitxml=$WORKSPACE/output/frontend_regression_firefox.xml || true
                    '''
                }
            }
            post { always { junit 'output/frontend_regression_firefox.xml' } }
        }

        // -------------------
        // Frontend Regression Chrome
        // -------------------
        stage('Frontend Regression Chrome') {
            steps {
                catchError(buildResult: 'UNSTABLE', stageResult: 'UNSTABLE') {
                    sh '''#!/bin/bash
                        set -xe
                        source my_venv/bin/activate
                        export PYTHONPATH=$WORKSPACE
                        export BROWSER=headlesschrome
                        cd demostore_automation
                        pytest tests/frontend/ --junitxml=$WORKSPACE/output/frontend_regression_chrome.xml || true
                    '''
                }
            }
            post { always { junit 'output/frontend_regression_chrome.xml' } }
        }
    }
}
