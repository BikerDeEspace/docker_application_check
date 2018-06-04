import Dockerfile as dockerfile
import config as conf

class Service:
    def __init__(self, service_name, data):
        self.errors = list()
        self.service_name = service_name
        self.data = data
        self.dockerfile = None

    def get_errors(self):
        return filter(None, self.errors)

    def get_element(self, data, key):
        return data[key] if key in data else None

    def check_build(self):
        build = self.get_element(self.data, 'build')
        if build:
            self.dockerfile = dockerfile.Dockerfile(build)
            return True
        else:
            return False



    def check_service(self):
        if self.check_build():
            self.dockerfile.get_result()