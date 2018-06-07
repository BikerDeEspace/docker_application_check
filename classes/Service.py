from conf.errors import DOCKERFILE_ERROR, SERVICE_ERROR, MAIN_ERROR_TEMPLATE

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

        self.nb_errors = 0

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
        """All service verification"""

        #Get dockerfile if exist
        dockerfile = self.get_dockerfile()

        if dockerfile:
            #DockerfileParser 
            dockerfile.check_dockerfile()

            #Service Validator
            validator = ServiceValidator(dockerfile.get_result(), self.service_data)
            validator.validate()

            #ERRORS TEXT FORMAT
            parser_errors = dockerfile.get_errors()
            validator_errors = validator.get_errors()

            #parser errors format
            if parser_errors:
                self.errors.append(MAIN_ERROR_TEMPLATE[2].format(nbErr=len(parser_errors), erreur="".join(parser_errors)))
            #validator errors format
            if validator_errors:
                self.errors.append(MAIN_ERROR_TEMPLATE[3].format(nbErr=len(validator_errors), erreur="".join(validator_errors)))

            #main errors format
            if self.errors:
                self.nb_errors = len(parser_errors) + len(validator_errors)
                self.errors = MAIN_ERROR_TEMPLATE[1].format(service=self.service_name, nbErr=self.nb_errors, erreur="".join(self.errors))