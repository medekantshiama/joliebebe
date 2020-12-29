import requests
from bs4 import BeautifulSoup


from io import BytesIO

myChoise = input("Entrez le numero d une categorie entre 1 et 50")
myChoise = int(myChoise)

choiseCategorie = input("entrez une categorie: ")
choiseCategorie = choiseCategorie.lower()

imageFile = open('image_of_categorie_'+choiseCategorie+'.img', 'w')

first_file = open('product_features'+choiseCategorie+'.csv', 'w')
first_file.write(
    'product_page_url  , upc, title,price_excluding_tax,number_available   ,  category   ,review_rating,image_url,  product_description\n')

mycategorie = []
html = requests.get('http://books.toscrape.com')
html.encoding = "utf-8"
response = html.text
soup = BeautifulSoup(html.text,'html.parser')
list_kind_category = []
kind_category = soup.findAll('ul')
for true_category in kind_category:
    list_kind = true_category.findAll('a')
    for very_kind in list_kind:
        list_kind_category.append(very_kind['href'])
        for very in very_kind:
            mycategorie.append(str(very))

for indice, cat in enumerate(mycategorie[1:52]):

    cat = cat.lower()

    if cat.strip() == (choiseCategorie):
        myChoise = int(indice)
        print(myChoise)

iter_category = list_kind_category[myChoise + 1]
second_response = requests.get('http://books.toscrape.com/' + iter_category)
second_response.encoding = "utf-8"
second_soup = BeautifulSoup(second_response.text,'html.parser')
info_article = second_soup.findAll('article')
for article in info_article:
    out = article.find('img')
    name = ''
    name = out['alt']

    attribute = article.find('p', {'class': "price_color"})
    for price in attribute:
        pass
    list_product = article.find('a')
    clean_list_product = list_product['href']
    link_product = 'http://books.toscrape.com/catalogue/' + clean_list_product[9:]
    page = requests.get(link_product)
    page.encoding = "utf-8"
    page_product = BeautifulSoup(page.text,'html.parser')
    find_upc = page_product.findAll('td')

    for upc in find_upc[0]:
        pass
    for availability in find_upc[5]:
        pass

    find_category = page_product.find('ul')
    list_category = find_category.findAll('a')
    for category in list_category[2]:
        str(category)

    find_review_rating = article.find('p')
    review_rating = str(find_review_rating)
    rating = review_rating[10:-137]  # j ai du couper ma chaine de caracteres pour ne retenir que le nombre d etoil
    image_url = 'http://books.toscrape.com' + str(out['src'])

    print(' nom du livre: ' + str(name) + '\n', 'son prix: ' + str(price), '\n',
              'le lien pour acceder au produit: ', '\n' + str(link_product), '\n', 'son code upc: ' + str(upc),'\n',
                      'Sa categorie: ' + str(category), '\n', 'Le nombre en stock: ' + str(availability), '\n',
                      '  Sa cotation en etoile: ' + str(rating), '\n', 'le lien pour l image: ', '\n',image_url[:25] + image_url[36:])
    find_description = page_product.findAll("p")
    description = str(find_description[3])
    print('sa description: ', description)
    print('____________________________________________________________')
    first_file.write(link_product + '_____' + category + '_____ ' + image_url+'______')
    first_file.write(upc + ',____')
    first_file.write(name + ',____')
    first_file.write(price + ',____')
    first_file.write(availability + ',____')
    first_file.write(category + '_____ ' + image_url + '______')
    first_file.write(rating + ',____')
    first_file.write(description + ',____')
    first_file.write('\n')

    imageResponse = requests.get(image_url[:25] + image_url[36:])

    imageFile.write(imageResponse.content)