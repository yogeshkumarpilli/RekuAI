pipeline{
    agent any

    stages{

        stage("Cloning from Github...."){
            steps{
                script{
                    echo 'Cloning from Github...'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/yogeshkumarpilli/RekuAI.git']])
                }
            }
        }

        stage("Set Up Virtual Environment") {
            steps {
                script {
                    echo 'Setting up Virtual Environment and Installing dependencies...'
                    sh '''
                        # Install uv package manager
                        curl -LsSf https://astral.sh/uv/install.sh | sh
                        . $HOME/.local/bin/env
                        
                        # Create and activate virtual environment
                        uv venv
                        . .venv/bin/activate
                        
                        # Install dependencies
                        uv sync
                        uv lock
                        uv build
                    '''
                }
            }
        }

        stage('DVC Pull'){
            steps{
                withCredentials([file(credentialsId:'gcp-key' , variable: 'GOOGLE_APPLICATION_CREDENTIALS' )]){
                    script{
                        echo 'DVC Pulling Stage....'
                        sh '''
                        . .venv/bin/activate
                        dvc pull
                        '''
                    }
                }
            }
        }
    }
}