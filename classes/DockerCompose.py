from conf.constant import DOCKER_COMPOSE_FILENAMES
from conf.errors import DOCKER_COMPOSER_ERROR

from classes import ServiceValidator

import yaml

from subprocess import  Popen, PIPE

class DockerCompose:
    def __init__(self, docker_compose_path, docker_compose_name = ''):

        self.data = None
        self.errors = list()
        self.docker_compose_path = docker_compose_path

        gen = (name for name in DOCKER_COMPOSE_FILENAMES if (docker_compose_path / name).exists)
        self.docker_compose_file = docker_compose_path / next(gen, None)
    
    def get_errors(self):
        return self.errors

    def get_service(self):
        with open(self.docker_compose_file, 'r') as stream:
            self.data = yaml.load(stream)    
        services = self.data['services']
        for service_name in services:
            yield ServiceValidator.Service(self.docker_compose_path, service_name, services[service_name])

    def check_file(self):
        process = Popen([
            'docker-compose', '-f', str(self.docker_compose_file), 'config', '--quiet'
        ], stdout=PIPE, stderr=PIPE)

        stdout, stderr = process.communicate()

        #if errors
        if stderr:
            self.errors.append(DOCKER_COMPOSER_ERROR[110].format(erreur=stderr.decode('utf-8')))
        else:
            for service in self.get_service():
                service.check_service()
                self.errors.extend(service.get_errors())
