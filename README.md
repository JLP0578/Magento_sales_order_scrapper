# Magento_sales_order_scrapper

Le script permet de parcourir les commandes en back-office prod, dev ou local.
Tous les éléments de la table `sales_order` de Magento, seront vérifié.

## Pourquoi ? 

Car de fil en aiguille, certaines commandes peuvent être altéré, une mise à jour de Magento 1 à Magento 2, un collègue qui supprime un produit en base de données.

## Installation

### Basic

Télécharger et installer [Python3](https://www.python.org/downloads/).
Durant l'installation cocher la case `pip`

pur installer les extentions requis faites : `pip install -r requirements.txt`

## Utilisation

Il est necéssaire d'avoir `Python3`, `pip`, et les extentions requis pour lancer le script.

Vérifié, que votre projet fraîchement cloné a les dossier `logs` et `output`, vous devrez aussi copier le `.env_sample`, renommez le en `.env` et renseignez les éléments

Exécuter `py ./main.py` pour lancer le script.
Il va vous demander sur quel environnement vous voulez qu'il travaille.

* [ ] prod
* [X] dev (par defaut)
* [] local

Et si vous voulez que le script arrête le poste à la fin.

* [ ] oui
* [X] non (par defaut)

Si le script trouve une erreur, il va générer un fichier dans `output`, il vous restera plus qu'à le réparer 🛠️

## Le `.env`


| Nom                    | Description                                             |
| ---------------------- | ------------------------------------------------------- |
| `PROD_HOST`            | **Ip** de la base de données de prod                    |
| `PROD_USER`            | **Utilisateur** de la base de données de prod           |
| `PROD_PASSWORD`        | **Mot de passe** de la base de données de prod          |
| `PROD_DATABASES`       | **Nom de la base**<br /> de la base de données de prod  |
| `PROD_DOMAIN`          | **URL** pour accéder au back-office de prod             |
| `PROD_USERNAME_LOGIN`  | **Utilisateur** pour accéder au back-office de prod     |
| `PROD_PASSWORD_LOGIN`  | **Mot de passe** pour accéder au back-office de prod    |
| `DEV_HOST`             | **Ip** de la base de données de dev                     |
| `DEV_USER`             | **Utilisateur** de la base de données de dev            |
| `DEV_PASSWORD`         | **Mot de passe** de la base de données de dev           |
| `DEV_DATABASES`        | **Nom de la base**<br /> de la base de données de dev   |
| `DEV_DOMAIN`           | **URL** pour accéder au back-office de dev              |
| `DEV_USERNAME_LOGIN`   | **Utilisateur** pour accéder au back-office de prod     |
| `DEV_PASSWORD_LOGIN`   | **Mot de passe** pour accéder au back-office de prod    |
| `LOCAL_HOST`           | **Ip** de la base de données du local                   |
| `LOCAL_USER`           | **Utilisateur** de la base de donnée du local           |
| `LOCAL_PASSWORD`       | **Mot de passe** de la base de données du local         |
| `LOCAL_DATABASES`      | **Nom de la base**<br /> de la base de données du local |
| `LOCAL_DOMAIN`         | **URL** pour accéder au back-office du local            |
| `LOCAL_USERNAME_LOGIN` | **Utilisateur** pour accéder au back-office du local    |
| `LOCAL_PASSWORD_LOGIN` | **Mot de passe** pour accéder au back-office du local   |
| `EXCLUDE_STORE`        | **ID** des store a exclure (ex :`"0, 3, 5"`)            |


## Quelles seraient les vulnérabilités de l'outil ? 

Les identifiants dans le .env et la connexion SSL, j'ai dû désactiver les erreurs pour le local