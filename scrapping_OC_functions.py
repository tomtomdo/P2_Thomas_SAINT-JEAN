import requests
from bs4 import BeautifulSoup

def recup_livres_categorie(url_category):
    """Fonction de récupération des adresses url des livres d'une catégorie.
        Cette fonction parcourt la page html d'une catégorie de livres et en extrait les adresses url des livres qui y sont listés.
        Elle détecte également la présence d'une page suivante, et, le cas échéant, en récupère également les adresses url des produits référencés.
        Le processus se poursuit jusqu'à qu'il ne soit plus détecté de page suivante.

        Parameter
        ---------
        url_category: str
            url de la page html de la catégorie de livres.
            
        Returns
        --------------------
        page_product_links: list
            La fonction produit une liste recensant les adresses url des livres de la catégorie parcourue.
    """

    page_product_links = []
    while True:
        response_category_page = requests.get(url_category)
        page_category = response_category_page.content
        soup_page_category = BeautifulSoup(page_category, "html.parser")
        #récupération des urls de la page dans une liste
        lines_containers = soup_page_category.find_all('div', class_="image_container")
        for line in lines_containers:
            a = line.find('a')
            link = a['href']
            link_splitted = link.split('/')
            link = "https://books.toscrape.com/catalogue/" + link_splitted[-2] + "/" + link_splitted[-1]
            page_product_links.append(link)

        #récupération de la page produits suivante dans la catégorie
        if soup_page_category.find('li', class_="next"):
            next = soup_page_category.find('li', class_="next").next_element
            next_link = next['href']
            url_category_splitted = url_category.split('/')
            url_category_splitted[-1] = next_link
            url_category = "/".join(url_category_splitted)
        else:
            break
    return page_product_links

def recuperation_infos_livre(url_livre):
    """Fonction de récupération des informations produits d'un livre.
        Cette fonction parcourt la page produit d'un livre et récupère les informations suivantes pour les stocker dans un dictionnaire:
        -l'url de la page produit du livre
        -le titre du livre
        -la description du livre
        -le code produit UPC (Universal Product Code)
        -la catégorie d'appartenance du livre
        -le prix hors taxes du livre
        -le prix taxes comprises du livre
        -la quantité disponible au moment de l'exécution du script
        -la note d'évaluation du livre
        -l'adresse url de l'icône du livre

        Parameters
        ----------
        url_livre : str
            url de la page produit du livre.

        Returns
        --------------------
        dict_book: dict
            Un dictionnaire recensant les informations récupérées. Les clés correspondent
            aux catégories des informations récupérées, les valeurs respectives, aux informations elles-mêmes.
    """
    #creation du dictionnaire de recueil
    dict_book = {}

    #remplissage du dictionnaire avec le reste des informations
    dict_book['product_page_url'] = url_livre

    #recuperation de la page html
    response = requests.get(url_livre)
    print("récupération des informations de la page en cours")
    if response.status_code !=  200:
        print("Page impossible a recuperer")
    else:
        print("Page recuperee avec succes")

    #transformation de la page en objet BeautifulSoup
    page = response.content
    soup = BeautifulSoup(page, "html.parser")

    #recuperation du titre du livre
    title = soup.find('div', class_="col-sm-6 product_main").find("h1")
    dict_book['title'] = title.string

    #recuperation de la description du livre
    descriptiontitre = soup.find("div", id="product_description")
    description_contenu = descriptiontitre.next_sibling.next_sibling
    dict_book['product_description'] = description_contenu.string

    #recuperation des informations produits
    product_informations = soup.find("table").find_all("td")
    dict_book['universal_product_code'] = product_informations[0].string
    dict_book['category'] = product_informations[1].string
    dict_book['price_excluding_tax'] = product_informations[2].string
    dict_book['price_including_tax'] = product_informations[3].string
    dict_book['number_available'] = product_informations[5].string

    #recuperation de l'evaluation du livre
    instock_availability = soup.find("p", class_="instock availability")
    review_rating = instock_availability.find_next("p")
    note = review_rating.attrs
    dict_book['review_rating'] = (note['class'][1])

    #recuperation de l'url de l'image du livre
    infos_image =soup.find("img")
    details_infos_image = infos_image.attrs
    dict_book['image_url'] = (details_infos_image['src'])

    return dict_book

