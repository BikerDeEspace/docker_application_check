import config as config

import Service as srv
import yaml

class DockerCompose:
    def __init__(self, docker_compose_path):
        self.errors = list()
        self.docker_compose_path = docker_compose_path
        self.data = None

    def get_service(self):
        gen = (name for name in config.DOCKER_COMPOSE_FILENAMES if (self.docker_compose_path / name).exists)
        with open(self.docker_compose_path / next(gen, None), 'r') as stream:
            data_loaded = yaml.load(stream)
            services = data_loaded['services']
            for service_name in services:
                yield srv.Service(service_name, services[service_name])

    def check_file(self):
        for service in self.get_service():
            service.check_service()
