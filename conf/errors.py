#
# ERRORS LISTS
#

MAIN_ERROR_TEMPLATE = {
    0 : 'APPLICATION | Erreur {nbErr} |\n',
    1 : '-> SERVICE "{service}" | Erreur {nbErr} |\n{erreur}',
    2 : '\tDOCKERFILE | Erreur {nbErr} | \n{erreur}',
    3 : '\tDOCKER COMPOSE | Erreur {nbErr} | \n{erreur}'
}

#DOCKER COMPOSE COMMAND
#Major errors catch by docker-compose commands
DOCKER_COMPOSER_ERROR = {
    110 :'DOCKER COMPOSE | CONFIG | Erreur |\n{erreur}',
    111 :'DOCKER COMPOSE | UP | Erreur | \n{erreur}'
}

#DOCKERFILE
#2** -- Dockerfile errors
#21* -- Dockerfile parser errors
#22* -- Dockerfile other errors 
DOCKERFILE_ERROR = {
    200 :'Erreur - Fichier introuvable : {chemin}',

    #errors template
    202 :'\t - L:{ligne} C:{colonne} | Instruction "{inst}" | {erreur}\n',

    211 :'Instruction: Instruction inconnue',
    212 :'Argument: Aucun argument spécifié',
    213 :'Argument: Syntaxe: argument1 argument2 …',
    214 :'Argument: Syntaxe: ["argument1", "argument2" …]',
    215 :'Argument: Actuel:{nombre} | Autorisés : Min:{min}, Max:{max}',
    216 :'Option: {opt} | Option inconnue',
    217 :'Option: {opt} | Option Incompatible avec l\'instruction',

    221 :'Instruction: Non spécifiée ou incorrecte',
    222 :'Instruction: ARG ou FROM doit être en première position',
    223 :'Elements: "{fichiers}" - Elements spécifiés introuvables',
    225 :'Port: "{expose_port}" - Syntaxe incorrecte'
}

#SERVICES
#Errors between Dockercompose & Dockerfile
SERVICE_ERROR = {
    302 :'\t - {erreur}\n',

    311 :'Port: Nombre Incorrect | Port configurés: {docker_compose_port}, Ports exposés: {dockerfile_ports}',
    312 :'Port: "{container_port}" - Non exposé dans le dockerfile'
}

