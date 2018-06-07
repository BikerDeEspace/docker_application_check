from conf.errors import SERVICE_ERROR


import re

class ServiceValidator:
    """
    Class who check the differences between dockerfile and docker-compose service
    """
    def __init__(self, dockerfile_data, service_data):
        self.errors = list()

        self.dockerfile_data = dockerfile_data
        self.service_data = service_data

        self.ports_checked = False

    def get_errors(self):
        """Return a list of formated errors from the validation process"""
        result = list()
        for error in self.errors: 
            result.append(SERVICE_ERROR[302].format(erreur=error))
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


    def get_dockerfile_inst(self, inst_name):
        """Return a list of dockerfile instruction"""
        result = list()
        for data in self.dockerfile_data:
            if data[0] == inst_name:
                result.extend(data[2])
        return result

    def get_docker_compose_inst(self, inst_name):
        """Return content of docker-compose instruction"""
        result = list()
        if inst_name in self.service_data:
            result = self.service_data[inst_name]
        return result

    #
    #   CHECKER
    #
    def ports(self, port1, port2):
        """Function who compare ports between the dockerfile and the service 

        Params :
        port1 -- List() -> Docker-compose.yml configured ports
        port2 -- List() -> Dockerfile exposed ports

        """
        #Only one check for this instruction is needed
        #TODO decorator ? 
        if not self.ports_checked:
            self.ports_checked = True
            #If number of ports are different
            if len(port1) != len(port2):
                self.errors.append(SERVICE_ERROR[311].format(docker_compose_port=len(port1), dockerfile_ports=len(port2)))
            #Expose port not present in ports configuration
            for port in port1:
                matches = re.search(r'(?<=:).*', port)
                if matches.group() not in port2:
                    self.errors.append(SERVICE_ERROR[312].format(container_port=matches.group()))



    #
    #   DOCKER_COMPOSE CHECK
    #       service_check_*
    #
    def service_check_ports(self, data):
        self.ports(data, self.get_dockerfile_inst('EXPOSE'))

    #
    #   DOCKERFILE CHECK
    #       docker_check_*
    #
    def docker_check_EXPOSE(self, data):
        self.ports(self.get_docker_compose_inst('ports'), self.get_dockerfile_inst('EXPOSE'))