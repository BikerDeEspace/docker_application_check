import sys

max = sys.maxsize

#
# INSTRUCTIONS
#

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
    'ARG'       : [1, 1, 1]
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

#Optional options before main instruction arguments
#OptionName : []
OPTIONAL_OPTION_CONFIG = {
    '--chown='  : ['COPY', 'ADD'],
    '--from='   : ['COPY']
}

#
# ERRORS LISTS
#

#DOCKER COMPOSE
#1** -- Docker-compose errors
#11* -- Docker-compose syntax errors
#12* -- Docker-compose other errors 
DOCKER_COMPOSER_ERROR = {
    100 :'DOCKER COMPOSE | Erreur - Fichier introuvable : {chemin}', 
    #Main syntax error template
    110 :'DOCKER COMPOSE | Erreur Syntaxe | L:{ligne} {erreur}',
    #Syntax errors messages

    #Other errors messages
    121 :'DOCKER COMPOSE | Aucun service défini'

}

#DOCKERFILE
#2** -- Dockerfile errors
#21* -- Dockerfile syntax errors
#22* -- Dockerfile other errors 
DOCKERFILE_ERROR = {
    200 :'DOCKERFILE | Erreur - Fichier introuvable : {chemin}',
    #Main syntax error template
    210 :'DOCKERFILE | Erreur Syntaxe | L:{ligne} C:{colonne} | Instruction "{inst}" | {erreur}',

    #Syntax errors messages
    201 :'Instruction inconnue',
    202 :'Aucun argument spécifié',
    203 :'Syntaxe des arguments: argument1 argument2 …',
    204 :'Syntaxe des arguments: ["argument1", "argument2" …]',
    205 :'Nombre d’arguments:{nombre} | Autorisés : Min:{min}, Max:{max}',
    206 :'Option: {opt} | Option inconnue',
    207 :'Option: {opt} | Option Incompatible avec l\'instruction',

    #Other errors messages
    221 :'DOCKERFILE | Erreur - Instruction {inst} non spécifiée ou incorrecte',
    222 :'DOCKERFILE | Erreur - Instruction {inst}: L\'instruction FROM doit être spécifiée en première',
    223 :'DOCKERFILE | Erreur - Instruction {inst}: "{fichiers}" Fichiers spécifiés introuvables',
    224 :'DOCKERFILE | Erreur - Instruction {inst}: Port:{expose_port} introuvable dans l’instruction ports du Docker-compose.yml ({container_ports})',
    225 :'DOCKERFILE | Erreur - Instruction {inst}: Port:{expose_port} syntaxe incorecte'
}

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
