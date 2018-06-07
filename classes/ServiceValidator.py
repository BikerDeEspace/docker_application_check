from conf.errors import DOCKERFILE_ERROR, DOCKER_COMPOSER_ERROR

class ServiceValidator:
    """
    Class who check the differences between dockerfile and docker-compose service
    """
    def __init__(self, dockerfile_data, service_data):
        self.errors = list()

        self.dockerfile_data = dockerfile_data
        self.service_data = service_data

    def get_errors(self):
        """Return errors list from the validation process"""
        return self.errors


    def get_dockerfile_inst(self, inst_name):
        """Return a list of dockerfile instruction"""
        result = list()
        for data in self.dockerfile_data:
            if data[0] == inst_name:
                result.append(data[2])
        return result

    def get_docker_compose_inst(self, inst_name):
        """Return a list of docker-compose instruction"""
        result = None
        if inst_name in self.service_data:
            result = self.service_data[inst_name]
        return result

    def validate(self):
        """Validation of a service check the difference between dockerfile and docker-compose"""

        #VERIF BY DOCKERFILE INSTRUCTIONS
        for data in self.dockerfile_data:
            try:
                getattr(self, "docker_check_%s" % data[0])(data[2])
            except AttributeError:
                pass

        #VERIF BY SERVICE CONFIGURATION
        for data in self.service_data:
            try:
                getattr(self, "service_check_%s" % data)(self.service_data[data])
            except AttributeError:
                pass

    #
    #   DOCKER_COMPOSE CHECK
    #       service_check_*
    #
    def service_check_ports(self, data):
        print('ports | expose ', self.get_dockerfile_inst('EXPOSE'))

    #
    #   DOCKERFILE CHECK
    #       docker_check_*
    #
    def docker_check_EXPOSE(self, data):
        print('expose | ports ', self.get_docker_compose_inst('ports'))