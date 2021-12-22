import csv

from scrapping_OC_functions import recuperation_infos_livre


#recuperation des informations d'un livre à partir de l'adresse url de sa page produit
url_livre = "https://books.toscrape.com/catalogue/sharp-objects_997/index.html"
dico_livre = recuperation_infos_livre(url_livre)

# création du document csv recensant les informations produit d'un livre
with open('infos_recueil.csv', 'w') as f:
    w = csv.DictWriter(f, dico_livre.keys())
    w.writeheader()
    w.writerow(dico_livre)