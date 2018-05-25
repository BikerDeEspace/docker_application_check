import DockerfileParser as dfp
import config as config

from subprocess import  Popen, PIPE

import yaml
import os
import re

#------------------
#verif_dockerfile
#------------------
def verif_dockerfile(path='./', container_port=None):
    """Fonction permettant de vérifier un fichier Dockerfile"""

    errors = list()
    dockerfile = dfp.DockerfileParser()
    dockerfile.parse(path)

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
        opt = parseResult[i][1]
        params = parseResult[i][2]
        opt_instruction = parseResult[i][3]

        #DEBUG
        print(parseResult[i])


        if not instruction_from and (instruction != 'FROM' and instruction != 'ARG'):
            errors.append(config.DOCKERFILE_ERROR[222].format(inst=instruction))
        
        if instruction == 'FROM':
            instruction_from = True
            #TODO image checking
        elif instruction == 'EXPOSE':
            instruction_expose = True
            #Check if expose ports equals ports in docker-compose.yml file
            if container_port and (container_port not in params):
                errors.append(config.DOCKERFILE_ERROR[224].format(expose_port=params))
        elif instruction == 'ADD' or instruction == 'COPY':
            #Check if files or folders exists
            if not os.path.exists(params[0]):
                errors.append(config.DOCKERFILE_ERROR[223].format(inst=instruction, fichiers=params[0]))

    #Required Instructions
    if not instruction_from:
        errors.append(config.DOCKERFILE_ERROR[221].format(inst='FROM'))
    if not instruction_expose:
        errors.append(config.DOCKERFILE_ERROR[221].format(inst='EXPOSE'))

    return errors

#------------------
#verif_docker_compose
#Supported filenames: docker-compose.yml, docker-compose.yaml, fig.yml, fig.yaml
#------------------
def verif_docker_compose():
    """Fonction permettant de vérifier un fichier docker-compose.yml"""
    errors = list()

    errors.extend(verif_dockerfile('./exemples/'))

    process = Popen(['docker-compose', 'config', '--quiet'], stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()

    if stderr:
        #TODO Extract errors
        print('++DOCKER COMPOSE ERR++')
        print(stderr)
    else:
        print(stdout)
        
        with open("docker-compose.yml", 'r') as stream:
            data_loaded = yaml.load(stream)

            #print(data_loaded['services']['app'])
            services = data_loaded['services']

            for serviceName in services:
                print(services[serviceName])

            
    return errors  

#------------------
#verif_logs
#------------------
def verif_logs():
    """Fonction permettant de vérifier les logs d'un conteneur"""
    errors = list()
    #DEBUT verif_logs
        #TANT QUE container FAIRE
            #Extraction Erreurs fichier de log

            #SI EXISTE Erreurs ALORS
                #Extraction des codes et des messages
        #FIN TANT QUE
    #FIN verif_logs
    return errors

#------------------
# Main
#------------------
def main():
    """Fonction principale du script de vérification"""
    errors = list()

    #Checking file docker-compose.yml
    errors.extend(verif_docker_compose())

    """ #Check if they are no errors
    if not errors:
        #Exec docker-compose up command
        process = Popen(['docker-compose', 'up', '-d'], stdout=PIPE, stderr=PIPE)
        stdout, stderr = process.communicate()

        #Check if they are no errors
        if stderr:
            #TODO  Extract errors (Function ?)
            print('ERR:',stderr)
        else:
            print(stdout)
            #Check the logs of each created container
            errors.extend(verif_logs()) """
    
    #Print errors and write it in a new log file
    print('++ERR++')
    for error in errors:
        print(error)
        
if __name__ == '__main__':
    main()