import sys
import re

from conf.errors import DOCKERFILE_ERROR

from pathlib import Path


class DockerfileValidator:
    """ DockerfileValidator
    Class who check each instruction arguments of a Dockerfile
    """
    
    def __init__(self, path):
        """DockerfileValidator constructor"""
        self.errors = list()
        self.instruction_from = False
        self.instruction_expose = False
        self.path = path

    def validate_instruction(self, inst):
        """Return true if the arguments are valid"""
        valid = True
        instruction_name = inst[0]
        instruction_params = inst[2]

        #Call verification function for this instruction if exist
        try:
            valid = getattr(self, "check_%s" % instruction_name)(instruction_params)
        except AttributeError:
            pass
            #print('Instruction :', instruction_name, 'non vérifiée')
        return valid



    def get_errors(self):
        """Return errors and clear list"""
        errors = "\n".join(self.errors)
        self.errors.clear()
        return errors

    #
    #   Usefull functions
    #
    def check_file(self, file):
        """Check if file or folder exist"""
        valid = True
        if file != '.':
            if not list(self.path.glob(file)):
                valid = False
                self.errors.append(DOCKERFILE_ERROR[223].format(fichiers=file))
        return valid

    #
    #   Instructions validators
    #
    def check_FROM(self, params):
        """Check arguments for FROM instruction"""
        valid = True
        #Accepted form : arg1 | arg1 AS arg2
        if len(params) == 2 or (len(params) == 3 and params[1] != 'AS'):
            valid = False
            self.errors.append(DOCKERFILE_ERROR[215].format(
                nombre=len(params), min=1, max=1, loc='{loc}'))
        return valid

    def check_ADD(self, params):
        """Check arguments for ADD instruction"""
        return self.check_file(params[0])

    def check_COPY(self, params):
        """Check arguments for COPY instruction"""
        return self.check_file(params[0])

    def check_EXPOSE(self, params):
        """Check arguments for EXPOSE instruction"""
        valid = True
        self.instruction_expose = True
        #Check if param syntax is correct (80[/tcp])
        for param in params:
            if not re.fullmatch(r'[0-9]+(\/(tcp|udp))?', param):
                valid = False
                self.errors.append(DOCKERFILE_ERROR[225].format(expose_port=param))
        return valid
    