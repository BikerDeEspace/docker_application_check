import DockerfileParser as dfp

class Dockerfile:
    def __init__(self, dockerfile_path):
        self.dockerfile_path = dockerfile_path
        self.parser = dfp.DockerfileParser()
        
    def get_inst(self, inst_name):
        instruction_list = list()
        for instruction in self.instructions:
            if instruction[2][0] == inst_name:
                instruction_list.append(instruction)
        return instruction_list
