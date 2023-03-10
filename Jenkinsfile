pipeline{
    
    agent any
    
    options{
        timestamps()
        disableConcurrentBuilds()
        timeout(time: 1, unit: 'HOURS')
    }

    parameters { booleanParam(name: 'Push_Image', defaultValue: false, description: 'push docker image or not?') }

    stages{
        stage('Clean'){
            steps{
                cleanWs()
            }
        }
        stage('Git pull'){
            steps{
               sh '''
               git clone https://github.com/dhutsj/python_demo.git
               '''
            }
        }
        stage('Docker Build'){
            steps{
                sh'''
                cd python_demo
                docker build -t dhutsj/python_demo:latest .
                '''
            }
        }
        stage('Docker push'){
            when  { expression { params.Push_Image } }
            steps{
                withCredentials([usernamePassword(credentialsId: 'my_dockerhub', passwordVariable: 'Password', usernameVariable: 'Username')]) {
                sh '''
                docker login -u${Username} -p${Password}
                docker push dhutsj/python_demo:latest
                '''
                }
            }
        }
    }

    post{
        always{
            script{
                println("always")
            }
        }
        success{
            script{
                currentBuild.description = "\n Run success!"
            }
        }
        failure{
            script{
                currentBuild.description = "\n Run failed!"
            }
        }
        aborted{
            script{
                currentBuild.description = "\n Aborted job!"
            }
        }
    }
}
