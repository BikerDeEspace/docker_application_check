from conf.errors import DOCKERFILE_ERROR

from classes.DockerfileParser import DockerfileParser
from classes.ServiceValidator import ServiceValidator

from conf.errors import DOCKERFILE_ERROR

class Service:
    """ 
    Class who represent a Service in the docker_compose.yml file
    """
    def __init__(self, path, service_name, service_data):
        self.errors = list()

        self.path = path
        self.service_name = service_name
        self.service_data = service_data

    def get_errors(self):
        """Return errors from the current service"""
        return self.errors

    def get_dockerfile(self):
        """Get the service dockerfile if exist"""
        dockerfile = None

        build = self.service_data['build']
        if build:
            #Check if build is not in short version
            if 'context' in build:
                dockerfile = DockerfileParser(self.path / build['context'])
            else:
                dockerfile = DockerfileParser(self.path / build)
                
        return dockerfile

    def check_service(self):
        """Control the service verifications"""

        #Get dockerfile if exist
        dockerfile = self.get_dockerfile()

        if dockerfile:
            #DockerfileParser 
            dockerfile.check_dockerfile()

            #Service Validator
            validator = ServiceValidator(dockerfile.get_result(), self.service_data)
            validator.validate()

            #Get errors from Parser and Validator
            self.errors.extend(dockerfile.get_errors())
            self.errors.extend(validator.get_errors())

            if self.errors: 
                self.errors.append(DOCKERFILE_ERROR[201].format(nbErr=len(self.errors), service=self.service_name, erreur="".join(self.errors)))