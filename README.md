# Magento_sales_order_scrapper

Ce script permet de parcourir en back-office tous les éléments de la table `sales_order` de Magento.

S'il en détecte une erreur, vous aurez un fichier de résultat dans `./output`

Les erreurs potentielles : 
- Vous avez supprimé un produit utilisé dans une commande et vous ne pouvez plus afficher la commande.
- Vous avez fait la migration de Magento 1 vers Magento 2 et certain élément de cardgift ne correspondent pas pour Magento 2
- Autre ?
