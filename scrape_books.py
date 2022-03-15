from urllib import response
import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
import os

links = []

dict_from_csv = pd.read_csv('category_books_urls.csv', header=None, index_col=0, squeeze=True).to_dict()


url = dict_from_csv["Travel"].replace("index.html", "page-") + str(1) + ".html" 
reponse = requests.get(url)
page = reponse.content
if reponse.ok:
    for i in range(9):
        url = dict_from_csv["Travel"].replace("index.html", "page-") + str(i) + ".html"   
        reponse = requests.get(url)
        page = reponse.content  
        soup = BeautifulSoup(page, "html.parser")

        h3s = soup.find_all("h3")
        for h3 in h3s:
            a = h3.find('a')
            link = a['href']
            links.append(url.replace("page-", "").replace(".html", "").replace(str(i), "") + link)
else :
    url = dict_from_csv["Travel"]
    reponse = requests.get(url)
    page = reponse.content
    soup = BeautifulSoup(page, "html.parser")

    h3s = soup.find_all("h3")
    for h3 in h3s:
        a = h3.find('a')
        link = a['href']
        links.append(url.replace("index.html", "") + link)


en_tete = ['product_page_url', 'upc', 'title', 'price_including_tax', 'price_excluding_tax', 'number_available', 'product_description', 'category', 'review_rating', 'image_url']
with open('category/Travel/Travel_books.csv', 'w') as csv_file:
    writer = csv.writer(csv_file, delimiter=',')
    writer.writerow(en_tete)
    for x in range(len(links)):
        url = links[x]
        reponse = requests.get(url)
        page = reponse.content
        if reponse.ok:
            soup = BeautifulSoup(page, "html.parser")

            upc = soup.find("th", text="UPC").find_next_sibling("td").string

            title = soup.find("h1").text

            price_including_tax = soup.find("th", text="Price (incl. tax)").find_next_sibling("td").string

            price_excluding_tax = soup.find("th", text="Price (excl. tax)").find_next_sibling("td").string

            number_available = soup.find("p", class_="instock availability").text.strip()

            review_rating = soup.find('p', class_='star-rating')
            review_rating = review_rating['class']
            review_rating = review_rating[1]

            category = soup.find("li").find_next_sibling("li").find_next_sibling("li").text.strip()

            product_description = soup.find("div", id="product_description").find_next_sibling("p").text

            image_url = soup.find("img")
            image_url = "https://books.toscrape.com/" + image_url['src']
            file = open('category/' + 'Travel/' + title[0:10] +".jpg", "wb")
            file.write(requests.get(image_url).content)
            file.close()

            writer = csv.writer(csv_file, delimiter=',')
                
            writer.writerow([url, upc, title, price_including_tax, price_excluding_tax, number_available, product_description, category, review_rating, image_url])    




