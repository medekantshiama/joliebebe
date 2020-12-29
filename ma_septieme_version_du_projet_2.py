

import requests

from bs4 import BeautifulSoup

import os
import shutil

from PIL import Image
from io import BytesIO

first_file = open('result.zip/product_characteristics.csv','w')
first_file.write(
    'product_page_url  , upc, title,price_excluding_tax, number available ,  category   ,review_rating,image_url,  product_description\n')

def getCategory(n):
    list_kind_category = []
    my_category = []
    response = requests.get('http://books.toscrape.com')

    response.encoding = "utf-8"
    soup = BeautifulSoup(response.text, 'html.parser')

    for true_category in soup.findAll('ul'):
        for very_kind in true_category.findAll('a'):
            list_kind_category.append(very_kind['href'])
            for very in very_kind:
                my_category.append(str(very))
    if n == 1:
        return list_kind_category
    elif n == 2:
        return my_category

for i, cat in enumerate(getCategory(2)[2:53]):

    def getCategoreiesUrls():
        soups = []
        categories = []

        categories.append('http://books.toscrape.com/'+ getCategory(1)[i+2])
        for index in range(2, 9):
            categories.append('http://books.toscrape.com/'+getCategory(1)[i+2][:-10] + 'page-' + str(index) + '.html')

        for index in categories:
            response = requests.get(index)
            if response.ok:
                response.encoding = "utf-8"
                second_soup = BeautifulSoup(response.text, 'html.parser')
                soups.append(second_soup.findAll('article'))

        return soups
    def getName():
        names = []
        for soup in getCategoreiesUrls():
            for article in soup:
                out = article.find('img')
                book_name = out['alt']
                names.append(book_name)
        return names
    print(getName())
    def getPrice():
        prices = []
        for soup in getCategoreiesUrls():
            for article in soup:
                attribute = article.find('p', {'class': "price_color"})
                for book_price in attribute:
                    prices.append(book_price)
        return prices

    def getProductsUrls(enter):
        page_urls = []
        link_product = []
        for soup in getCategoreiesUrls():
            for article in soup:
                list_product = article.find('a')['href']

                link_product.append('http://books.toscrape.com/catalogue/' + list_product[9:])
                page_url = requests.get('http://books.toscrape.com/catalogue/' + list_product[9:])
                page_url.encoding = "utf-8"
                page_soup = BeautifulSoup(page_url.text, 'html.parser')
                page_urls.append(page_soup)
        if enter == 1:
            return link_product
        elif enter == 2:
            return page_urls

    def getUpcAndAvailability(enter):
        all_upc = []
        availabilities = []

        for page_soup in getProductsUrls(2):

            for book_upc in page_soup.findAll('td')[0]:
                all_upc.append(book_upc)
            for book_availability in page_soup.findAll('td')[5]:
                availabilities.append(book_availability)
        if enter == 1:
            return all_upc

        elif enter == 2:
            return availabilities

    def getRating():
        ratings = []
        for soup in getCategoreiesUrls():
            for article in soup:
                find_review_rating = article.find('p')
                review_rating = str(find_review_rating)
                rating = review_rating[10:-137]
                ratings.append(rating)
        return ratings

    def getImageUrl():
        image_urls = []
        for soup in getCategoreiesUrls():
            for article in soup:
                book_image_url = 'http://books.toscrape.com' + article.find('img')['src'][11:]
                image_urls.append(book_image_url)
        return image_urls


    def getDescription():
        descriptions = []
        for find_description in getProductsUrls(2):
            book_description = find_description.findAll("p")
            descriptions.append(book_description[3])
        return descriptions
    print(cat.strip())
    file = 'result.zip/product_characteristics_of_caterorie_'+ str(cat.strip()) +'.csv'
    first_file = open(file,'w')
    first_file.write(
        'product_page_url  , upc, title,price_excluding_tax, number available ,  category   ,review_rating,image_url,  product_description\n')
    for size in range(len(getName())):
        first_file.write(getName()[size]+',   ')
        first_file.write('price: '+ getPrice()[size] + ',  ')
        first_file.write('upc: ' + getUpcAndAvailability(1)[size]+ ',  ')
        first_file.write('number available: ' + getUpcAndAvailability(2)[size]+',  ')
        first_file.write('product_page_url: '+ getProductsUrls(1)[size]+',  ')
        first_file.write('review_rating: '+ getRating()[size]+ ',  ')
        first_file.write('image_url: '+ getImageUrl()[size] + '\n')
        first_file.write('product_description: ' + str(getDescription()[size])+ '\n')

    for url, name in zip(getImageUrl(), getName()):
        response = requests.get(url)
        good_name = "".join([char for char in name if char.isalnum()])
        image_name = 'C:/Users/Random/PycharmProjects/pythonProject2/joliebebe-scrape1/result.zip/image_of_categorie_'+cat + good_name + '.jpg'
        with open(image_name, 'wb') as image_file:
             image_file.write(response.content)