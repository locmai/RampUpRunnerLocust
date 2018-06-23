pipeline {
  agent any
  stages {
    stage('SCM') {
      steps {
        echo 'Start cloning'
        git url: 'https://github.com/locmai/RampUpRunnerLocust.git'
        echo 'Cloning ended'
      }
    }
  }
}
