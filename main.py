#Dockerfile parser
import Dockerfile as dfp
import DockerCompose as dockerC
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

#--------------------
# Main
#--------------------
def main():
    """Fonction principale du script de vérification"""
    errors = list()

    docker_compose_path = config.DOCKER_PROJECTS_PATH / input('Enter docker-compose file folder: ')
    
    #Checking file docker-compose.yml
    docker_compose = dockerC.DockerCompose(docker_compose_path)
    docker_compose.check_file()

    errors.extend(docker_compose.get_errors())

    #Check if no errors
    if not errors:
        #Exec docker-compose up command
        process = Popen(['docker-compose','-f', str(docker_compose_path), 'up', '-d'], stdout=PIPE, stderr=PIPE)
        stdout, stderr = process.communicate()

        #Check if no errors
        if stderr:
            errors.append(config.DOCKER_COMPOSER_ERROR[111].format(erreur=stderr.decode('utf-8')))

    if errors:
        #Write errors in a log file 
        # - filename : %Y-%m-%d_%H-%M-%S
        f = open('logs/{time}.txt'.format(
            time=strftime("%Y-%m-%d_%H-%M-%S", gmtime())
        ),'w') 

        f.writelines(errors)
        f.close()

        #Print errors
        print("".join(errors))
        
        
if __name__ == '__main__':
    main()