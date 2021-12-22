import requests
from bs4 import BeautifulSoup


#fonction de recuperation des informations d'un livre
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

        Paramètre
        ----------
        url_livre : str
            url de la page produit du livre

        Production en sortie
        ----------
        Un dictionnaire recensant les informations récupérées. Les clés correspondent
        aux catégories des informations récupérées, les valeurs respectives, aux informations elles-mêmes.
        """
    #creation du dictionnaire de recueil
    dico_livre = {}

    #remplissage du dictionnaire avec le reste des informations
    dico_livre['product_page_url'] = url_livre

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
    dico_livre['title'] = title.string

    #recuperation de la description du livre
    descriptiontitre = soup.find("div", id="product_description")
    description_contenu = descriptiontitre.next_sibling.next_sibling
    dico_livre['product_description'] = description_contenu.string

    #recuperation des informations produits
    product_informations = soup.find("table").find_all("td")
    dico_livre['universal_product_code'] = product_informations[0].string
    dico_livre['category'] = product_informations[1].string
    dico_livre['price_excluding_tax'] = product_informations[2].string
    dico_livre['price_including_tax'] = product_informations[3].string
    dico_livre['number_available'] = product_informations[5].string

    #recuperation de l'evaluation du livre
    instock_availability = soup.find("p", class_="instock availability")
    review_rating = instock_availability.find_next("p")
    note = review_rating.attrs
    dico_livre['review_rating'] = (note['class'][1])

    #recuperation de l'url de l'image du livre
    infos_image =soup.find("img")
    details_infos_image = infos_image.attrs
    dico_livre['image_url'] = (details_infos_image['src'])

    return dico_livre

