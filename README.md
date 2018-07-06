# Script de vérification 

Ce script de vérification vérifie la valité et la cohérence des informations renseignées dans un les les fichiers Dockerfile et dans le fichier Docker-compose.

Il effectue également une vérification syntaxique de ces fichiers. 

# CONFIGURATION 

-> Fichier conf/constant.py 

Assurez vous d'avoir indiqué un repertoire correct pour vos applications docker-compose. Car le script effectue ses vérifications a partir de cet emplacement.

# INSTALLATION

-> Certaines dépendances renseignées dans le fichier requirement.txt sont nécessaires pour le bon fonctionnemt du script 

    pip install requirement.txt