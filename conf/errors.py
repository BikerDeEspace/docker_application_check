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
    224 :'Port: "{expose_port}" - Introuvable dans l’instruction ports du Docker-compose.yml ({container_ports})',
    225 :'Port: "{expose_port}" - Syntaxe incorrecte'
}

#SERVICES
#Errors between Dockercompose & Dockerfile
SERVICE_ERROR = {

}