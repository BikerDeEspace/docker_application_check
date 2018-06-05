import sys

max = sys.maxsize

#
# INSTRUCTIONS
#
#Main instruction
#InstructionName : [ArgumentsFormCode, ArgumentsNumMin, ArgumentsNumMax]
#ArgumentsFormCode :
# -- 1: Simple List forms (Ex: arg1 arg2)
# -- 2: Table forms (Ex: ["arg1", "arg2"])
# -- 3: All possible forms
INSTRUCTION_CONFIG_LIST = {
    'FROM'      : [1, 1, 3], 
    'RUN'       : [3, 1, max], 
    'ADD'       : [3, 2, 2], 
    'COPY'      : [3, 2, 2], 
    'EXPOSE'    : [1, 1, max], 
    'CMD'       : [3, 1, max], 
    'ENTRYPOINT': [3, 1, 3], 
    'VOLUME'    : [3, 1, max], 
    'WORKDIR'   : [3, 1, 1],
    'LABEL'     : [1, 1, max],
    'USER'      : [1, 1, max],
    'ARG'       : [1, 1, 1],
    'SHELL'     : [2, 1, max],
    'ENV'       : [1, 1, max]
}

#Options before main instruction arguments
#OptionName : []
OPTIONAL_OPTION_CONFIG = {
    '--chown='  : ['COPY', 'ADD'],
    '--from='   : ['COPY']
}

#Optional instructions after main instruction arguments
#InstructionName : [ArgumentsFormCode, ArgumentsNumMin, ArgumentsNumMax]
#ArgumentsFormCode :
# -- 1: Simple List forms (Ex: arg1 arg2)
# -- 2: Table forms (Ex: ["arg1", "arg2"])
# -- 3: All possible forms
OPTIONAL_INSTRUCTION_CONFIG = {
    'AS': ['FROM']
}