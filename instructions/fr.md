
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

  - **C'EST À DIRE:**
 
    - Si vous êtes une compétence dev et un maître copie que vous voulez traduire, plutôt que de traduire une compétence active
qui peuvent avoir coutume énoncés etc dans.

Tapez le chemin ** ** A la compétence, mais ** PAS ** la skillname. (Utiliser le champ skillTitle pour cela)

PAR EXEMPLE:

- Skillpath = / home / pi / DevelopmentSkills
- skillTitle = HomeAssistant
.

## ** SkillTitle champ ** (obligatoire)

Ce champ indique la compétence que vous voulez traduire

- Avec ce champ rempli et ** ** PAS le * Skillpath * champ et puis les paramètres par défaut de chemin vers le ProjectAlice / dossier compétences
- Avec ce domaine et sur le terrain Skillpath ** PAS ** Complété vous traduirez cette compétence par défaut ..
_
## ** ** translateOnlyThis

Pour ce domaine ...

- Vide = traduirai tous les fichiers requis (par défaut)

- Entrez l'un des éléments suivants pour traduire uniquement ce dossier (facultatif)
 - des pourparlers
 - dialogue
 - instructions_______________________

Bugs #Known

L'exécution de la compétence une fois devrait fonctionner comme prévu, mais d'essayer de l'exécuter deux fois sans redémarrer Alice
résultat d'une erreur « langue non valide ».

**Exemple**:

1. Lancez le mode precheck et laissez la compétence exécution de la tâche de ce
2. Accédez aux paramètres et désactiver le mode PreCheck
3. Exécutez le processus de traduction et ALICE montrera dans les journaux que l'ensemble de la langue dans les paramètres
est « invalide » malgré elle pas changé.

Pour résoudre:

1. Redémarrez Alice et exécuter le mode de traduction à nouveau

- Note de côté:

 si vous ne vous arrive d'obtenir cette erreur régulièrement ..
 
 `` `Json.decoder.JSONDecodeError: valeur Grossesse: ligne 1 colonne 1 (char 0)` ``
 
 Ensuite, potentiellement, Goggle vient bloquer votre adresse IP à partir de fichiers traduction et vous devrez attendre jusqu'à ce que le temps du Pacifique de minuit suivant pour qu'il soit débloquée t

------------------

Google translate a tendance à aimer en ajoutant des espaces où les espaces n'était pas auparavant. Bien que cette compétence à la capture trys
certaines de ces occasions, vous pouvez constater que lors de la traduction des instructions dossier que si vous avez des balises dans le démarquage
que vous pourriez avoir à prendre manuellement certains espaces blancs pour avoir afficher correctement.

** Qu'est-ce que la compétence ne fera pas **

Actuellement, la compétence ne se traduira pas des fichiers Markdown tels que ces instructions. C'est une caractéristique de l'avenir à ajouter

Profitez de la traduction