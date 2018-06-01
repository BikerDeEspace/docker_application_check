class Service:
    def __init__(self, service_name, data):
        self.errors = list()
        self.service_name = service_name
        self.data = data
        self.dockerfile = None

    def get_element(self, data, key):
        return data[key] if key in data else None

    def check_build(self):
        build = self.get_element(self.data, 'build')
        if build:
            context = self.get_element(build, 'context')
            if context:
                #Verif dockerfile
                pass
            else:
                #Verif dockerfile
                pass
                
    def check_port(self):
        ports = self.get_element(self.data, 'ports')
        if ports:
            pass

    def check_service(self):
        pass