from conf.errors import DOCKERFILE_ERROR

from classe import DockerfileParser

from conf.errors import DOCKERFILE_ERROR

class Service:
    """ 
    Class who represent a Service in the docker_compose.yml file
    """
    def __init__(self, path, service_name, data):
        self.errors = list()

        self.path = path
        self.service_name = service_name
        self.data = data
        self.dockerfile = None

    def get_errors(self):
        return self.errors

    def get_element(self, data, key):
        return data[key] if key in data else None

    def check_build(self):
        build = self.get_element(self.data, 'build')
        if build:
            #Check if build is not in short version
            #Check dockerfile linked to the service
            if 'context' in build:
                self.dockerfile = DockerfileParser.DockerfileParser(self.path / build['context'])
            else:
                self.dockerfile = DockerfileParser.DockerfileParser(self.path / build)


    def check_service(self):
        self.check_build()

        self.dockerfile.check_dockerfile()
        errors = self.dockerfile.get_errors()
        if errors: 
            self.errors.extend(DOCKERFILE_ERROR[201].format(nbErr=len(errors), service=self.service_name, erreur="".join(errors)))