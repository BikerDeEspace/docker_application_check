import sys

max = sys.maxsize

#InstructionName : [ArgumentsFormCode, ArgumentsNumMin, ArgumentsNumMax]
#ArgumentsFormCode :
# -- 1: Simple List forms (Ex: arg1 arg2)
# -- 2: Table forms (Ex: ["arg1", "arg2"])
# -- 3: All possible forms
INSTRUCTION_CONFIG_LIST = {
    'FROM': [1, 1, 1], 
    'RUN': [3, 1, max], 
    'ADD': [2, 2, 2], 
    'COPY': [1, 2, 2], 
    'EXPOSE': [1, 1, max], 
    'CMD': [3, 1, max], 
    'ENTRYPOINT': [3, 1, 3], 
    'VOLUME': [3, 1, 1], 
    'WORKDIR': [3, 1, 1]
}

#Error List
DOCKERFILE_ERROR = {
    200 :'DOCKERFILE | Erreur - Fichier introuvable : {chemin}',
    #Main error template
    210 :'DOCKERFILE | Erreur Syntaxe | L:{ligne} {erreur}',

    #Sub syntax errors template
    201 :'C:{colonne} | Instruction "{inst}" | Instruction inconnue',
    202 :'C:{colonne} | Instruction "{inst}" | Aucun argument spécifié',
    203 :'C:{colonne} | Instruction "{inst}" | Syntaxe des arguments: argument1 argument2 …',
    204 :'C:{colonne} | Instruction "{inst}" | Syntaxe des arguments: [‘’argument1’’, ‘’argument2’’ …]',
    205 :'C:{colonne} | Instruction "{inst}" | Nombre d’arguments:{nombre} | Autorisés : Min:{min}, Max:{max}',

    #Logical errors template
    251 :'DOCKERFILE | Erreur - Instruction {inst} non spécifiée',
    252 :'DOCKERFILE | Erreur - La première instruction doit être FROM',
    253 :'DOCKERFILE | Erreur - Instruction {inst}: "{fichiers}" Fichiers spécifiés introuvables',
    254 :'DOCKERFILE | Erreur - EXPOSE: Port:{expose_port} introuvable dans l’instruction ports du Docker-compose.yml ({container_ports})'
}

DOCKER_COMPOSER_ERROR = {
    
}