class ServiceValidator:

    def __init__(self, dockerfile_data, service_data):
        self.errors = list()

        self.dockerfile_data = dockerfile_data
        self.service_data = service_data

    def get_errors(self):
        return self.errors

    def validate(self):
        
        print('++dockerfile++')
        for data in self.dockerfile_data:
            print(data)

        print('++service++')
        for data in self.service_data:
            print(data)