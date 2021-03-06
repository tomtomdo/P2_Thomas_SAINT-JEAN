import requests
from bs4 import BeautifulSoup


def rec_category_books_urls(category_url):
    """Fonction de récupération des adresses url des livres d'une catégorie.
        Cette fonction parcourt la page html d'une catégorie de livres et en extrait les adresses url des livres
        qui y sont listés.
        Elle détecte également la présence d'une page suivante, et, le cas échéant, en récupère également les adresses
         url des produits référencés.
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
        response_category_page = requests.get(category_url)
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
            next_line = soup_page_category.find('li', class_="next").next_element
            next_link = next_line['href']
            url_category_splitted = category_url.split('/')
            url_category_splitted[-1] = next_link
            category_url = "/".join(url_category_splitted)
        else:
            break
    return page_product_links


def rec_book_details(book_url):
    """Fonction de récupération des informations produits d'un livre.
        Cette fonction parcourt la page produit d'un livre et récupère les informations suivantes pour les stocker
        dans un dictionnaire:
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
        book_url : str
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
    dict_book['product_page_url'] = book_url

    #recuperation de la page html
    response = requests.get(book_url)
    book_url_splitted = book_url.split("/")
    book_name = book_url_splitted[-2]

    print(f"Récupération des informations produit du livre {book_name} en cours")
    if response.status_code != 200:
        print(f"Page {book_name} impossible a récupérer")
    else:
        print(f"Page {book_name} récupérée avec succès")

    #transformation de la page en objet BeautifulSoup
    page_book = response.content
    soup_page_book = BeautifulSoup(page_book, "html.parser")

    #recuperation du titre du livre
    title = soup_page_book.find('div', class_="col-sm-6 product_main").find("h1")
    dict_book['title'] = title.string

    #recuperation de la description du livre
    if soup_page_book.find("div", id="product_description"):
        title_description = soup_page_book.find("div", id="product_description")
        content_description = title_description.next_sibling.next_sibling
        dict_book['product_description'] = content_description.string
    else:
        dict_book['product_description'] = "description de contenu absente"

    #recuperation des informations produits
    product_informations = soup_page_book.find("table").find_all("td")
    dict_book['universal_product_code'] = product_informations[0].string
    dict_book['category'] = product_informations[1].string
    dict_book['price_excluding_tax'] = product_informations[2].string
    dict_book['price_including_tax'] = product_informations[3].string
    dict_book['number_available'] = product_informations[5].string

    #recuperation de l'evaluation du livre
    instock_availability = soup_page_book.find("p", class_="instock availability")
    review_rating = instock_availability.find_next("p")
    note = review_rating.attrs
    dict_book['review_rating'] = (note['class'][1])

    #recuperation de l'url de l'image du livre
    infos_image = soup_page_book.find("img")
    infos_image_details = infos_image.attrs
    image_url_incomplete = infos_image_details['src']
    image_url_incomplete_splitted = image_url_incomplete.split("/")
    image_url = "https://books.toscrape.com/media/cache/" + image_url_incomplete_splitted[-3] + "/" + \
                image_url_incomplete_splitted[-2] + "/" + image_url_incomplete_splitted[-1]
    dict_book['image_url'] = image_url
    return dict_book
