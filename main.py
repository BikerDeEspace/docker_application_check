import DockerComposeParser as dcp
import DockerfileParser as dfp
import config as config

import yaml
import os
import re

def verif_dockerfile(path='./', filename='Dockerfile', container_port=None):
    """Fonction permettant de vérifier un fichier Dockerfile"""

    errors = list()
    #Parsing
    dockerfile = dfp.DockerfileParser()
    dockerfile.parse(path, filename)

    if(dockerfile.hasError()):
        errors.extend(dockerfile.error)

    parseResult = dockerfile.fileparsed
    
    instruction_from = False
    instruction_expose = False

    #Foreach instruction
    # -- Inst[i][0] = Instruction name (never null)
    # -- Inst[i][1] = arguments list (never null)
    for i in range(0, len(parseResult)):
        instruction = parseResult[i][0]
        params = parseResult[i][1]

        print(parseResult[i])

        #Instructions à vérifier 
        # -- FROM : Instruction en 1ère position && image disponible
        # -- EXPOSE : Port correct && 
        # -- COPY && ADD : Fichiers sources existants
        if i == 0 and instruction != 'FROM':
            errors.append(config.DOCKERFILE_ERROR[252])
        if instruction == 'FROM':
            instruction_from = True
        elif instruction == 'EXPOSE':
            instruction_expose = True
            #port exposés correspondant à un des ports du fichier docker-compose
            if(container_port and (container_port not in params)):
                errors.append(config.DOCKERFILE_ERROR[254].format(expose_port=params))
        elif instruction == 'ADD' or instruction == 'COPY':
            #verification de l'existance des dossiers ou fichiers indiqués
            if not os.path.exists(params[0]):
                errors.append(config.DOCKERFILE_ERROR[253].format(inst=instruction, fichiers=params[0]))

    #Vérification instructions obligatoires
    if not instruction_from:
        errors.append(config.DOCKERFILE_ERROR[251].format(inst='FROM'))
    if not instruction_expose:
        errors.append(config.DOCKERFILE_ERROR[251].format(inst='EXPOSE'))

    return errors

def verif_docker_compose():
    """Fonction permettant de vérifier un fichier docker-compose.yml"""
    errors = list()

    #Parsing
    docker_compose = dcp.DockerComposeParser()
    docker_compose.parse()

    if(docker_compose.hasError()):
        errors.extend(docker_compose.error)
    else:
        print("DOCKER COMPOSE")
        with open("exemples/docker-compose.yml", 'r') as stream:
            data_loaded = yaml.load(stream)
            services = data_loaded['services']

            print(data_loaded['services'])
            for serviceName in services:
                service = data_loaded['services'][serviceName]
                print(serviceName + ' - ' + str(service))


        #Vérifications 
        # -- Il existe au moins un service
        # -- Chaque service est basé sur une image ou un dockerfile associé
        #       -> Image disponible
        #       -> Dockerfile : Verifications
        # -- Au moins un service communique avec la machine hôte
        #TODO Verifications 

        print("DOCKERFILE")
        errors.extend(verif_dockerfile('exemples/'))


    return errors

    #TODO


def verif_logs():
    """Fonction permettant de vérifier les logs d'un conteneur"""
    errors = list()

    return errors

def main():
    """Fonction principale du script de vérification"""
    errors = list()

    #On verifie le fichier docker-compose.yml
    errors.extend(verif_docker_compose())

    #On vérifie qu'il n'existe pas d'erreurs
    if not errors:
        #On lance la création de l'application

        #On teste les fichiers de logs
        errors.extend(verif_logs())
    
    #On affiche les erreurs dans la console & On les inscrits dans un fichier de log
    counter = 1
    for error in errors:
        print(counter,'-',error)
        counter += 1
        

main()