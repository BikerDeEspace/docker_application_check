import sys
from pathlib import Path

max = sys.maxsize

#
# FILEPATH
#
DOCKER_PROJECTS_PATH = Path(r"C:\Users\llegrand\Documents\DockerProjects")

#
# FILENAMES
#
DOCKER_COMPOSE_FILENAMES = [
    "docker-compose.yml", 
    "docker-compose.yaml", 
    "fig.yml", 
    "fig.yaml"
]

DOCKERFILE_FILENAMES = [
    "Dockerfile",
    "dockerfile"
]

#
# INSTRUCTIONS
#
#Optional instruction before main instruction
OPTIONAL_INSTRUCTION = {
    'ONBUILD'
    'HEALTHCHECK'
}

#Main instruction
#InstructionName : [ArgumentsFormCode, ArgumentsNumMin, ArgumentsNumMax]
#ArgumentsFormCode :
# -- 1: Simple List forms (Ex: arg1 arg2)
# -- 2: Table forms (Ex: ["arg1", "arg2"])
# -- 3: All possible forms
INSTRUCTION_CONFIG_LIST = {
    'FROM'      : [1, 1, 1], 
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
    '--from='   : ['COPY'],

    '--interval=': ['HEALTHCHECK'],
    '--timeout=': ['HEALTHCHECK'],
    '--start-period=': ['HEALTHCHECK'],
    '--retries=': ['HEALTHCHECK']
}

#Optional instructions after main instruction arguments
#InstructionName : [ArgumentsFormCode, ArgumentsNumMin, ArgumentsNumMax]
#ArgumentsFormCode :
# -- 1: Simple List forms (Ex: arg1 arg2)
# -- 2: Table forms (Ex: ["arg1", "arg2"])
# -- 3: All possible forms
OPTIONAL_INSTRUCTION_CONFIG = {
    'AS': [1, 1, 1]
}

#
# ERRORS LISTS
#

#DOCKER COMPOSE
#Major errors catch by docker-compose config
DOCKER_COMPOSER_ERROR = {
    110 :'DOCKER COMPOSE | CONFIG | Erreur |\n{erreur}',

    111 :'DOCKER COMPOSE | UP | Erreur | \n{erreur}'
}

#DOCKERFILE
#2** -- Dockerfile errors
#21* -- Dockerfile parser errors
#22* -- Dockerfile other errors 
DOCKERFILE_ERROR = {
    200 :'DOCKERFILE | Erreur - Fichier introuvable : {chemin}',

    #Main dockerfile errors template
    201 :'DOCKERFILE | Erreur {nbErr} | Service "{service}" | \n{erreur}',
    #errors template
    202 :'\t - L:{ligne}\t C:{colonne} \t| Instruction "{inst}" \t| {erreur}\n',

    #Parser errors messages
    211 :'Instruction: Instruction inconnue',
    212 :'Argument: Aucun argument spécifié',
    213 :'Argument: Syntaxe: argument1 argument2 …',
    214 :'Argument: Syntaxe: ["argument1", "argument2" …]',
    215 :'Argument: Actuel:{nombre} | Autorisés : Min:{min}, Max:{max}',
    216 :'Option: {opt} | Option inconnue',
    217 :'Option: {opt} | Option Incompatible avec l\'instruction',
   
    #script errors messages
    221 :'Instruction: Non spécifiée ou incorrecte',
    222 :'Instruction: ARG ou FROM doit être en première position',
    223 :'Elements: "{fichiers}" - Elements spécifiés introuvables',
    224 :'Port: "{expose_port}" - Introuvable dans l’instruction ports du Docker-compose.yml ({container_ports})',
    225 :'Port: "{expose_port}" - Syntaxe incorrecte'
}