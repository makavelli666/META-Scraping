# Social Media Collector

Ce script Python vous permet de collecter des posts à partir de Facebook et Instagram en fonction d'une requête donnée, stockant les données dans une base de données MongoDB.

## Configuration des Tokens

Avant d'utiliser le script, assurez-vous de configurer les tokens d'accès pour Facebook et Instagram dans le fichier `main.py`.


## Utilisation

    Installez les dépendances nécessaires en exécutant la commande suivante :


pip install instaloader facebook-sdk pymongo

    Exécutez le script main.py pour collecter des posts de Facebook et Instagram.

python main.py

Assurez-vous que MongoDB est en cours d'exécution localement et accessible à l'adresse mongodb://localhost:27017/.
