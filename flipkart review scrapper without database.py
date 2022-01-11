from os import write
import re
from pymongo import results
import requests
from urllib.request import urlopen as ureq
from bs4 import BeautifulSoup as bs
import pandas as pd
import json



search= input('Enter the product name: ').replace(' ','')


flipkart_url= 'https://www.flipkart.com/search?q='
uclient= requests.get(flipkart_url+search)
#page_html= uclient.read()
#uclient.close()
flipkart_html= bs(uclient.content, 'html.parser')
product_= flipkart_html.find_all('div', {'class':"_2kHMtA"})

url= 'https://www.flipkart.com'

for i in product_:
    new_product_link= url+i.find('a')['href']


iclient= requests.get(new_product_link)
item_html= bs(iclient.content, 'html.parser')
item_= item_html.find_all('div', {'class':"_1YokD2 _2GoDe3"})

item_name= []
item_price= []
item_rating= []
item_specs= []
item_reviews= []

for item in item_:
    name= item.find('div',{'class': '_2NKhZn'})
    ratings= item.find('div',{'class': '_3LWZlK'})
    price= item.find('div',{'class': '_30jeq3 _16Jk6d'})
    specs= item.find('div',{'class': '_2418kt'})


    if name and ratings and price and specs is not None:
        item_name.append(name.text)
        item_rating.append(ratings.text)
        item_price.append(price.text.replace('₹', 'Rs. '))
        item_specs.append(specs.text)


reviewboxes= item_html.find_all('div', {'class':"_16PBlm"})

for i in reviewboxes:
    reviews= i.find('div', {'class': 't-ZTKy'})
    
    if reviews is not None:
        item_reviews.append(reviews.text)

    else:
        item_reviews.append('N/A')


mydict= {'Name': item_name, 'Price': item_price, 'Ratings': item_rating, 'Specifications': item_specs, 'Review': item_reviews, 'Reviews': item_reviews}

with open('Scrapped data/'+search+".json", "w") as outfile:
    json.dump(mydict, outfile)





