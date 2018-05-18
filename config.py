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
    'FROM'      : [3, 1, 1], 
    'RUN'       : [3, 1, max], 
    'ADD'       : [3, 2, 2], 
    'COPY'      : [3, 2, 2], 
    'EXPOSE'    : [1, 1, max], 
    'CMD'       : [3, 1, max], 
    'ENTRYPOINT': [3, 1, 3], 
    'VOLUME'    : [3, 1, 1], 
    'WORKDIR'   : [3, 1, 1]
}

#
# ERRORS LISTS
#

#DOCKER COMPOSE
#1** -- Docker-compose errors
#11* -- Dockerfile syntax errors
#12* -- Dockerfile other errors 
DOCKER_COMPOSER_ERROR = {
    100 :'DOCKER COMPOSE | Erreur - Fichier introuvable : {chemin}', 
    #Main syntax error template
    210 :'DOCKER COMPOSE | Erreur Syntaxe | L:{ligne} {erreur}',
    #Syntax errors messages

    #Other errors messages

}

#DOCKERFILE
#2** -- Dockerfile errors
#21* -- Dockerfile syntax errors
#22* -- Dockerfile other errors 
DOCKERFILE_ERROR = {
    200 :'DOCKERFILE | Erreur - Fichier introuvable : {chemin}',
    #Main syntax error template
    210 :'DOCKERFILE | Erreur Syntaxe | L:{ligne} {erreur}',

    #Syntax errors messages
    201 :'C:{colonne} | Instruction "{inst}" | Instruction inconnue',
    202 :'C:{colonne} | Instruction "{inst}" | Aucun argument spécifié',
    203 :'C:{colonne} | Instruction "{inst}" | Syntaxe des arguments: argument1 argument2 …',
    204 :'C:{colonne} | Instruction "{inst}" | Syntaxe des arguments: [‘’argument1’’, ‘’argument2’’ …]',
    205 :'C:{colonne} | Instruction "{inst}" | Nombre d’arguments:{nombre} | Autorisés : Min:{min}, Max:{max}',

    #Other errors messages
    221 :'DOCKERFILE | Erreur - Instruction {inst} non spécifiée',
    222 :'DOCKERFILE | Erreur - La première instruction doit être FROM',
    223 :'DOCKERFILE | Erreur - Instruction {inst}: "{fichiers}" Fichiers spécifiés introuvables',
    224 :'DOCKERFILE | Erreur - EXPOSE: Port:{expose_port} introuvable dans l’instruction ports du Docker-compose.yml ({container_ports})'
}
