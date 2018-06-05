#Dockerfile parser
import DockerfileParser as dfp
#config file
import config as config

#Log files names
from time import gmtime, strftime
#stderr catching
from subprocess import  Popen, PIPE
#path manipulation
from pathlib import Path

#docker-compose file parsing
import yaml
#input
import os
#regex
import re

#------------------
#verif_dockerfile
#------------------
def verif_dockerfile(path='./', service='', container_port=None):
    """Fonction permettant de vérifier un fichier Dockerfile"""
    dockerfile = dfp.DockerfileParser()
    errors = list()
    errors.extend(dockerfile.parse(path))

    instruction_from   = False
    instruction_expose = False
    #Foreach instruction
    # -- Inst[i][0] = Instruction line (never null)
    # -- Inst[i][1] = instruction [
    #       -- [0] InstructionName (never null)
    #       -- [1] OptionsList
    #       -- [2] ArgumentsList (never null)
    #       -- [3] OptionalInstructionsList
    #    ] (never null)
    parsefile = dockerfile.fileparsed
    for i in range(0, len(parsefile)):

        #Current instruction data
        line_number = str(parsefile[i][0])
        complete_instruction = parsefile[i][1]
        instruction = complete_instruction[0]
        params = complete_instruction[2]
        #opt = complete_instruction[1]
        #opt_instruction = complete_instruction[3]

        print(line_number, '++', instruction, '++', complete_instruction)

        #Instruction error template
        inst_error_template = config.DOCKERFILE_ERROR[202].format(
            ligne=line_number, colonne='..', inst=instruction, erreur='{erreur}'
        )

        if not instruction_from and (instruction != 'FROM' and instruction != 'ARG'):
            errors.append(inst_error_template.format(
                erreur=config.DOCKERFILE_ERROR[222])
            )

        if instruction == 'FROM':
            instruction_from = True
            #TODO image checking
        elif instruction == 'EXPOSE':
            instruction_expose = True
            #Check if param syntax is correct (80[/tcp])
            if not re.fullmatch(r'[0-9]+(\/(tcp|udp))?', params[0]):
                errors.append(inst_error_template.format(
                    erreur=config.DOCKERFILE_ERROR[225].format(expose_port=params[0]))
                )
            #Check if expose ports equals ports in docker-compose.yml file
            elif container_port and (container_port not in params):
                errors.append(inst_error_template.format(
                    erreur=config.DOCKERFILE_ERROR[224].format(expose_port=params))
                )
        elif instruction == 'ADD' or instruction == 'COPY':
            #Check if files or folders exists
            if not list(path.glob(params[0])):
                errors.append(inst_error_template.format(
                    erreur=config.DOCKERFILE_ERROR[223].format(fichiers=params[0]))
                )

    #Required Instructions
    if not instruction_from:
        errors.append(config.DOCKERFILE_ERROR[202].format(
            ligne='..', colonne='..', inst='FROM', erreur=config.DOCKERFILE_ERROR[221]
        ))
    if not instruction_expose:
        errors.append(config.DOCKERFILE_ERROR[202].format(
            ligne='..', colonne='..', inst='EXPOSE', erreur=config.DOCKERFILE_ERROR[221]
        ))
    
    return None if not errors else config.DOCKERFILE_ERROR[201].format(nbErr=len(errors), service=service, erreur="".join(errors)) 

#--------------------
#verif_docker_compose
#Supported filenames: docker-compose.yml, docker-compose.yaml, fig.yml, fig.yaml
#--------------------
def verif_docker_compose(path):
    """Fonction permettant de vérifier un fichier docker-compose.yml"""
    errors = list()

    gen = (name for name in config.DOCKER_COMPOSE_FILENAMES if (path / name).exists)
    file = path / next(gen, None)

    #Check syntax and main logic of docker-compose file
    process = Popen([
        'docker-compose', '-f', str(file), 'config', '--quiet'
    ], stdout=PIPE, stderr=PIPE)

    stdout, stderr = process.communicate()

    #if errors
    if stderr:
        errors.append(config.DOCKER_COMPOSER_ERROR[110].format(erreur=stderr.decode('utf-8')))
    else: 
        #If no errors check docker-compose, extract main infos & check dockerfiles
        with open(file, 'r') as stream:
            data_loaded = yaml.load(stream)
            services = data_loaded['services']


            for serviceName in services:
                service_content = services[serviceName]
                for element in service_content:
                    print('--', element)
                print(service_content, '++' , serviceName)
                #Check if exist build configuration
                if 'build' in service_content:
                    build = service_content['build']
                    #Check if build is not in short version
                    #Check dockerfile linked to the service
                    #if 'context' in build:
                    #    errors.append(verif_dockerfile(path / build['context'], serviceName))
                    #else:
                    #    errors.append(verif_dockerfile(path / build, serviceName))

    return filter(None, errors)

#--------------------
#verif_logs
#--------------------
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

#--------------------
# Main
#--------------------
def main():
    """Fonction principale du script de vérification"""
    errors = list()

    docker_compose_path = config.DOCKER_PROJECTS_PATH / input('Enter docker-compose file folder: ')
    
    #Checking file docker-compose.yml
    errors.extend(verif_docker_compose(docker_compose_path))

    #Check if no errors
    if not errors:
        #Exec docker-compose up command
        process = Popen(['docker-compose','-f', str(docker_compose_path), 'up', '-d'], stdout=PIPE, stderr=PIPE)
        stdout, stderr = process.communicate()

        #Check if no errors
        if stderr:
            errors.append(config.DOCKER_COMPOSER_ERROR[111].format(erreur=stderr.decode('utf-8')))
        else:
            print(stdout)
            #Check the logs of each created container
            errors.extend(verif_logs())

    if errors:
        #Write errors in a log file 
        # - filename : %Y-%m-%d_%H-%M-%S
        """ f = open('logs/{time}.txt'.format(
            time=strftime("%Y-%m-%d_%H-%M-%S", gmtime())
        ),'w') 

        f.writelines('\n'.join(errors))
        f.close() """

        #Print errors
        print("".join(errors))
        
        
if __name__ == '__main__':
    main()