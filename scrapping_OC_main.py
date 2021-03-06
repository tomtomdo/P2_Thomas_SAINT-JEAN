import csv
import requests
from bs4 import BeautifulSoup
import os
import shutil

from scrapping_OC_functions import rec_book_details, rec_category_books_urls

#récupération des liens urls des catégories de livres et enregistrement de celles-ci dans une liste.
url_books_to_scrape = "https://books.toscrape.com/index.html"
response_web_site = requests.get(url_books_to_scrape)
print("Récupération de la page d'accueil du site en cours")
if response_web_site.status_code != 200:
    print("Page d'accueil impossible a récupérer")
else:
    print("Page d'accueil récupérée avec succès")
home_page = response_web_site.content
soup_home_page = BeautifulSoup(home_page, "html.parser")
nav_list = soup_home_page.find('ul', class_="nav")
links_categories = nav_list.find_all('a')
categories_urls_list = []
for link_category in links_categories:
    link_category = "https://books.toscrape.com/" + link_category["href"]
    categories_urls_list.append(link_category)
categories_urls_list.pop(0)
print("Liste des catégories de livre constituée")


#récupération des url des livres pour chaque catégorie du site
for category_url in categories_urls_list:
    category_books_dicts_list = []
    category_url_splitted = category_url.split("/")
    category_name = category_url_splitted[-2]
    os.mkdir(f"Icones_{category_name}")
    print(f"======================Récupération des livres de la catégorie {category_name} en cours====================")
    category_books_urls = rec_category_books_urls(category_url)
    #Constitution d'une liste de dictionnaires par catégorie. Un dictionnaire contient les données produit d'un livre
    for book_url in category_books_urls:
        book_dict = rec_book_details(book_url)
        category_books_dicts_list.append(book_dict)
        book_url_splitted = book_url.split("/")
        book_name = book_url_splitted[-2]
        if len(book_name) > 100:
            book_name = (book_name.split("-"))[0] + "_" + (book_name.split("-"))[1] + "_" + (book_name.split("-"))[2]
        #récupération des icones produit des différents livres
        image_url = book_dict['image_url']
        r = requests.get(image_url, stream=True)
        if r.status_code != 200:
            print(f"Icone {book_name} impossible à récupérer")
        else:
            print(f"Icone {book_name} récupérée avec succès")
        with open(f"Icone_{book_name}.jpg", 'wb') as f:
            f.write(r.content)
        source = f"Icone_{book_name}.jpg"
        target = f"Icones_{category_name}"
        shutil.move(source, target)

    #écriture des données produit des livres de chaque catégorie dans des fichiers .csv disctincts
    with open(f"Infos_recueil_{category_name}.csv", 'w', encoding="utf-8") as f:
        w = csv.DictWriter(f, book_dict.keys())
        w.writeheader()
        for book_dict in category_books_dicts_list:
            w.writerow(book_dict)
