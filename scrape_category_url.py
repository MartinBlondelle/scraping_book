
import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
import os

url="https://books.toscrape.com/"
reponse = requests.get(url)
page = reponse.content
soup = BeautifulSoup(page, "html.parser")

links = []
name_category = []


# permet d'aller récupérer les liens des catégories
for ultag in soup.find_all('ul', class_='nav nav-list'):
    for litag in ultag.find_all('li'):    
        a = litag.find('a')
        link = a['href']
        links.append("https://books.toscrape.com/" + link)

# permet d'aller récupérer le nom des catégories       
for ultag in soup.find_all('ul', class_='nav nav-list'):
    for litag in ultag.find_all('li'):    
        a = litag.find('a')
        category = a.text
        name_category.append(category.replace("\n","").replace(" ",""))

# suppression le premier lien et le premier nom des listes
del links[0]
del name_category[0]



# création d'un csv avec le nom des catégories dans une column et leurs liens dans une autre
en_tete = ['name_category', 'link']
with open('category_books_urls.csv', 'w') as csv_file:
    writer = csv.writer(csv_file, delimiter=',')
    writer.writerow(en_tete)
    for category, link in zip(name_category, links):
        writer.writerow([category, link])

# création du dossier category
os.makedirs('category')

# création des dossiers par nom de catégorie
for name in name_category:
    str(name)
    os.makedirs('category/'+ name)