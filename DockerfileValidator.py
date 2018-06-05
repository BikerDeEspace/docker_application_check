from pathlib import Path

import config as config
import sys
import re

class DockerfileValidator:
    """ DockerfileValidator

    Check each instruction arguments of a Dockerfile
    """
    
    def __init__(self, path):
        self.errors = list()
        self.instruction_from = False
        self.instruction_expose = False
        self.path = path

    def validate_instruction(self, inst):
        valid = True
        instruction_name = inst[0]
        instruction_params = inst[2]

        #Call verification function for this instruction if exist
        try:
            valid = getattr(self, "check_%s" % instruction_name)(instruction_params)
        except AttributeError:
            print('Instruction :', instruction_name, 'non vérifiée')
        return valid

    def get_errors(self):
        errors = "\n".join(self.errors)
        self.errors.clear()
        return errors


    def check_file(self, file):
        """Check if file or folder exist"""
        valid = True
        if not list(self.path.glob(file)):
            valid = False
            self.errors.append(config.DOCKERFILE_ERROR[223].format(fichiers=file))
        return valid

    #
    #   Instructions validators
    #
    def check_FROM(self, params):
        valid = True
        #Accepted form : arg1 | arg1 AS arg2
        if len(params) == 2 or (len(params) == 3 and params[1] != 'AS'):
            valid = False
            self.errors.append(config.DOCKERFILE_ERROR[215].format(
                nombre=len(params), min=1, max=1, loc='{loc}'))
        return valid

    def check_ADD(self, params):
        return self.check_file(params[0])

    def check_COPY(self, params):
        return self.check_file(params[0])

    def check_EXPOSE(self, params):
        valid = True
        self.instruction_expose = True
        #Check if param syntax is correct (80[/tcp])
        for param in params:
            if not re.fullmatch(r'[0-9]+(\/(tcp|udp))?', param):
                valid = False
                self.errors.append(config.DOCKERFILE_ERROR[225].format(expose_port=param))
        return valid
    