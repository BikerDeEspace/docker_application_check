#Error List
DOCKERFILE_ERROR = {
    200 :'DOCKERFILE | Erreur - Fichier introuvable : {chemin}',
    
    201 :'DOCKERFILE | L:{ligne} C:{colonne} | Erreur Syntaxe - Instruction "{inst}" inconnue',
    202 :'DOCKERFILE | L:{ligne} C:{colonne} | Erreur Syntaxe | Syntaxe d’une instruction : INSTRUCTION [Arguments]',
    203 :'DOCKERFILE | L:{ligne} C:{colonne} | Erreur Syntaxe | Syntaxe des arguments: argument1 argument2 …',
    204 :'DOCKERFILE | L:{ligne} C:{colonne} | Erreur Syntaxe | Syntaxe des arguments: [‘’argument1’’, ‘’argument2’’ …]',
    205 :'DOCKERFILE | L:{ligne} C:{colonne} | Erreur Syntaxe | Nombre d’arguments:{nombre} | Autorisés : Min:{min}, Max:{max}',

    206 :'DOCKERFILE | Erreur - Instruction FROM non spécifiée',
    207 :'DOCKERFILE | Erreur - Instruction EXPOSE non spécifiée',
    208 :'DOCKERFILE | Erreur - COPY: {fichiers} Fichiers spécifiés introuvables',
    209 :'DOCKERFILE | Erreur - ADD: {fichiers} Fichiers spécifiés introuvables',
    210 :'DOCKERFILE | Erreur - EXPOSE: Port:{expose_port} introuvable dans l’instruction ports du Docker-compose.yml ({container_ports})'
}

DOCKER_COMPOSER_ERROR = {
    
}