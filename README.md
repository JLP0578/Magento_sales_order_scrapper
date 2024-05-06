# Magento_sales_order_scrapper

Ce script permet de parcourir en back-office tous les éléments de la table `sales_order` de Magento.

## Pourquoi ? 
Car de fil en aiguille, certaines commandes peuvent être altéré, une mise à jour de Magento 1 à Magento 2, un collègue qui supprime un produit en base de données.

## Comment sa marche ? 
Vérifié, que votre projet fraîchement cloné a les dossier `logs` et `output`, vous devrez aussi copier le `.env_sample`, renommez le en `.env` et renseignez les éléments

J'ai mis a disposition 3 type de connexion : 
- Prod
- Dev
- Local

Vous avez aussi la possibilité d'exclure certains stores.

Pour lancer le script faites un `py ./main.py`, choisissez le type de connexion puis si vous voulez éteindre l'ordinateur à la fin de la procédure.

Si le script trouve une erreur, il va générer un fichier dans `output`, il vous restera plus qu'à le réparer 🛠️

## Quelles seraient les vulnérabilités de l'outil ? 
Les identifiants dans le .env et la connexion SSL, j'ai dû désactiver les erreurs pour le local
