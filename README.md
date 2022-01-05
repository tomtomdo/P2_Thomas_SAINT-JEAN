# Scrapping python du site Books to Scrape: Scrapping_OC
***
***
## Présentation générale du programme
Scrapping OC est un programme dont le but est de récupérer automatiquement les données produit de l'intégralité des livres 
proposés par le site de vente en ligne Books to Scrape.

## Configuration compatible
Le programme a été conçu et validé pour la configuration suivante:\
*Version Python: 3.9\
*Version OS/PC: Windows 10/x64
## Installation du programme
L'installation se déroule selon les étapes suivantes:
1. Installer Python 3.9.\
Se rendre sur le site Python.org, dans la section downloads afin d'y télécharger la dernière version de Python 3.9.\
Lien de la page: <https://www.python.org/downloads/>
2. Intégrer le chemin d'accès du programme Python au PATH Windows afin que Python soit accessible depuis n'importe quel emplacement.
3. Créer un dossier d'accueil pour l'environnement virtuel dans lequel s'exécutera le programme.
4. Créer l'environnement virtuel.\
Le gestionnaire d'environnement virtuel ***venv*** est installé nativement lors de l'installation de Python.\
Pour créer un environnement virtuel, ouvrir une invite de commande, se rendre dans le dossier crée à l'étape précédente, et saisir la commande suivante:\
`py -m venv votreenvironnement`
5. Activer l'environnement virtuel\
Se rendre dans le dossier de l'environnement virtuel, puis dans le dossier ***Scripts***. Y saisir la commande: `activate.bat`\
L'activation est constatable par l'apparition de l'expression ***(votreenvironnement)*** en début de ligne.
6. Initialiser le contrôle de version git.\
Saisir la commande: `git init`
7. Rappatrier le code source depuis le dépôt distant GitHub.\
Saisir la commande: `git clone https://github.com/tomtomdo/P2_Thomas_SAINT-JEAN.git`
8. Se rendre dans le dossier projet **P2_Thomas_SAINT-JEAN** et y Installer les packages nécessaires au fonctionnement du programme par la commande: `pip install -r requirements.txt`


## Fonctionnalités
Le programme réalise des opérations ETL (Extract Transform Load) à différents endroits du site, et termine par un chargement des \
données dans des fichiers csv ou dossiers.\
La page d'accueil est la première parcourue pour récupérer les adresses url des catégories de livres. Puis pour chaque page catégorie\
les étapes suivantes sont réalisées :
1. Depuis la page d'accueil du site, liste des catégories de livre. 
2. Depuis chaque page catégorie, liste des pages produits qui y sont référencées.
3. Pour chaque page produit, récupération des informations suivantes :
    - Adresse url du livre
    - Code UPC du livre
    - Titre du livre
    - Prix HT
    - Prix TTC
    - Quantité disponible
    - Catégorie du produit
    - Note d'évaluation
    - Adresse url de l'icône de couverture
4. Récupération de l'image de couverture du livre et enregistrement dans un dossier contenant les images des couvertures de la catégorie.
5. Écriture de données produit des livres dans des fichiers .csv. Un fichier .csv est généré par catégorie.

## Démarrage du programme
1. Si des données ont déjà été produites, veiller à les supprimer avant de lancer le programme pour éviter des conflits de doublons de fichiers.
2. Ouvrir l'invite de commande windows
3. Répéter l'étape 5. du paragraphe "Installation du programme" pour activer l'environnement virtuel.
4. Se placer dans le répertoire **P2_Thomas_SAINT-JEAN** et saisir la commande `py scrapping_OC_main.py`\

## Données produites par le programme
* Les données produit de chaque livre sont récupérées et enregistrées dans un fichier .csv, à raison d'un 
fichier .csv par catégorie de livre.\
* Les icones de couverture des livres sont elles aussi récupérées et sauvegardées dans des dossiers, à raison d'un dossier par catégorie également.\
* Précision concernant cette étape: tout titre de livre dépassant 100 caractères (espaces compris) est raccourci de telle sorte que seule les premiers mots qui le constituent\
sont conservés dans le nom final de l'image qui sera stocké dans le dossier de sauvegarde.\
* Durant son exécution, le script affiche sa progression par des messages rendant compte de la catégorie travaillée et du livre dont les informations sont en cours de récupération.\
* Les données produites se trouvent dans le dossier **P2_Thomas_SAINT-JEAN**.