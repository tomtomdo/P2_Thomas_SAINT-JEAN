import csv

from scrapping_OC_functions import recuperation_infos_livre, recup_livres_categorie


#récupération des liens url des produits d'une catégorie
url_category = "https://books.toscrape.com/catalogue/category/books/mystery_3/index.html"
urls_livre = recup_livres_categorie(url_category)

#création d'une liste recensant les informations des livres d'une catégorie
liste_dico_livres = []
for url_livre in urls_livre:
    dico_livre = recuperation_infos_livre(url_livre)
    liste_dico_livres.append(dico_livre)

# écriture des informations de la liste des livres d'une catégorie dans un fichier csv
with open('infos_recueil.csv', 'w') as f:
    w = csv.DictWriter(f, liste_dico_livres[0].keys())
    w.writeheader()
    for dico in liste_dico_livres:
        w.writerow(dico)