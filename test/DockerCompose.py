import config as config

import Service as srv
import yaml

class DockerCompose:
    def __init__(self, docker_compose_path, docker_compose_name):

        self.data = None
        self.errors = list()

        if docker_compose_name != '':
            gen = (name for name in config.DOCKER_COMPOSE_FILENAMES if (docker_compose_path / name).exists)
            self.docker_compose_path = docker_compose_path / next(gen, None)
        else:
            self.docker_compose_path / docker_compose_path

    def get_service(self):
        with open(self.docker_compose_path, 'r') as stream:
            self.data = yaml.load(stream)
            
        services = self.data['services']
        for service_name in services:
            yield srv.Service(service_name, services[service_name])

    def check_file(self):
        for service in self.get_service():
            service.check_service()
