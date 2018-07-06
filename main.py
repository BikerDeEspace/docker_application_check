from classes.DockerfileParser import DockerfileParser
from classes.DockerCompose import DockerCompose

from conf.constant import DOCKER_PROJECTS_PATH
from conf.errors import DOCKER_COMPOSER_ERROR

from time import gmtime, strftime
from subprocess import  Popen, PIPE
from pathlib import Path

#input
import os

#--------------------
# Main
#--------------------
def main():
    """Fonction principale du script de vérification"""
    errors = list()

    docker_compose_path = DOCKER_PROJECTS_PATH / input('Enter docker-compose file folder: ')
    
    #Checking file docker-compose.yml
    docker_compose = DockerCompose(docker_compose_path)
    

    #Check if no errors
    if docker_compose.check_file():
        pass
        """#Exec docker-compose up command
        process = Popen(['docker-compose','-f', str(docker_compose.docker_compose_file) , 'up', '-d'], stdout=PIPE, stderr=PIPE)
        stdout, stderr = process.communicate()

        #Check if no errors
        if stderr:
            errors.append(DOCKER_COMPOSER_ERROR[111].format(erreur=stderr.decode('utf-8'))) """
    else:
        errors.append(docker_compose.get_errors())

    if errors:
        #Write errors in a log file 
        # - filename : %Y-%m-%d_%H-%M-%S
        """ f = open('logs/{time}.log'.format(
            time=strftime("%Y-%m-%d_%H-%M-%S", gmtime())
        ),'w', encoding = "UTF-8") 
        f.writelines(errors)
        f.close() """

        #Print errors
        print("".join(errors))
        
        
if __name__ == '__main__':
    main()