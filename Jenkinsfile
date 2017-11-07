def pythons = ["2.7.14", "3.5.4", "3.6.2"]

def steps = pythons.collectEntries {
    ["python $it": job(it)]
}

parallel steps

node {
    stage("Build Docker Sample") {
        docker.build("nickbabcock/bottle-ssl")
    }
}

def job(version) {
    return {
        docker.image("python:${version}").inside {
            checkout scm
            sh 'useradd --no-create-home --no-user-group BottleUser'
            sh 'echo BottleUser:iambottle | chpasswd'
            sh 'openssl req -new -x509 -days 365 -nodes -out cacert.pem -keyout privkey.pem -subj "/C=AA/ST=State/L=Location/O=IT/CN=bottle-ssl.com"'
            sh 'pip install pipenv'
            sh 'pipenv install --dev --verbose'
            sh 'pipenv run pytest --junitxml=TestResults.xml'
            junit 'TestResults.xml'
        }
    }
}