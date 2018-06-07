from conf.constant import DOCKER_COMPOSE_FILENAMES
from conf.errors import DOCKER_COMPOSER_ERROR, MAIN_ERROR_TEMPLATE

from classes.Service import Service

import yaml

from subprocess import  Popen, PIPE

class DockerCompose:
    """
    Class who reprensent docker-compose.yml file
    """
    def __init__(self, docker_compose_path, docker_compose_name = ''):

        self.data = None
        self.errors = list()
        self.docker_compose_path = docker_compose_path

        gen = (name for name in DOCKER_COMPOSE_FILENAMES if (docker_compose_path / name).exists)
        self.docker_compose_file = docker_compose_path / next(gen, None)
    
    def get_errors(self):
        """Return errors list from the validation process"""

        return self.errors

    def get_service(self):
        """Service Generator - Return each services object""" 

        with open(self.docker_compose_file, 'r') as stream:
            self.data = yaml.load(stream)    
        services = self.data['services']
        for service_name in services:
            yield Service(self.docker_compose_path, service_name, services[service_name])

    def check_file(self):
        """Validate a docker-compose file and start the validation process"""

        #First check of the docker-compose.yml file by the config command
        process = Popen([
            'docker-compose', '-f', str(self.docker_compose_file), 'config', '--quiet'
        ], stdout=PIPE, stderr=PIPE)

        stdout, stderr = process.communicate()

        #if errors
        if stderr:
            self.errors.append(DOCKER_COMPOSER_ERROR[110].format(erreur=stderr.decode('utf-8')))
        else:
            #Check each service of the docker-compose file
            for service in self.get_service():
                service.check_service()
                self.errors.extend(service.get_errors())
