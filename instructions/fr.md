# <Span style = "color: #FF0000;"> <strong> Instructions </span> </strong>

Donc, vous avez écrit une compétence et que vous voulez le traduire? Bon travail, permet d'obtenir en elle alors.

# <Span style = "color: #0000FF;"> <strong> étapes opérationnelles rapides </span> </strong>

** Pour utiliser cette compétence **

1. Accédez aux paramètres de compétences

2. Entrez le nom de la compétence que vous voulez traduire en ** ** skillTitle champ

3. Cliquez sur Enregistrer

Demandez alice à « traduire mes compétences »

# <Span style = "color: #0000FF;"> <strong> Savoir-faire Vue d'ensemble </span> </strong>

- Mode PreCheck
 
Cela se déroulera à travers le processus de traduction sans réellement envoyer des données de traduction Google.
Il est une course factice qui ne modifie pas les fichiers mais donner une rétroaction statistique à la fin du processus.

Ce mode utilise le fichier de langue la compétence a été écrit dans (jeu via ... paramètres compétences >> skillLanguage) pour déterminer les statistiques sur le processus de traduction
avant d'envoyer ces données à Google. De cette façon, vous pouvez prendre une décision éclairée si

1. il y a des erreurs dans les fichiers qui arrêtera le processus de traduction

2. Les fichiers sont dans les limites des quotas de Goggle ou sur ses limites et donc déclencheront les gardes de sécurité intégrés

Une fois l'exécution et montre aucune erreur, désactiver ce mode pour exécuter la compétence en mode traduction


## ** Lorsqu'il est exécuté en mode de traduction: **

La compétence se traduira par le répertoire des discussions en premier. Si les demandes vers Google dépassent le quota, il sera
mettre en pause le code pendant 70 secondes (Pause la compétence non Alice), puis reprendre.

La compétence sera alors traduire le fichier de dialogue et faire les mêmes gardes de sécurité de quotas. (Note: Si le nombre de caractères
pour une instance dépassera probablement 1500 le code pause pendant 1 heure)

Lors de la traduction de dialogue modèle le code extrait la partie: => keyValue} des énoncés
de sorte que le keyValue ne marche pas se traduire et arrêter l'habileté de travailler. Il est ensuite mis que le code backin
avant de l'écrire dans un fichier.

Une fois traduit ajoutera ensuite les 4 langues au fichier d'installation.

## ** Skillpath champ ** (en option)

- Ceci est pratique vous voulez traduire vos fichiers de compétences qui sont en dehors du dossier des compétences

