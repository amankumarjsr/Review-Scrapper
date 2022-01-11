from os import write
import re
from pymongo import results
import requests
from urllib.request import urlopen as ureq
from bs4 import BeautifulSoup as bs
import pandas as pd
import json
import pymongo
from pymongo import MongoClient


import certifi
ca = certifi.where()

# Connection Established to MongoDB
client = MongoClient(f"mongodb+srv://aman:<password>@cluster0.<change it to >.mongodb.net/ReviewScrapper?retryWrites=true&w=majority", tlsCAFile=ca)
db = client['ReviewScrapper']
collection= db['data']

#taking input
srch=input('Enter the product name: ')
search= srch.replace(' ','')

#checking if data is in database or not
check_data= collection.find_one({'_id': srch})
if check_data is not None:
    id= check_data['_id']


    if srch == id:
        data =collection.find_one({'_id': srch})
        print ('Data already avialable in database')

        with open('Scrapped data/'+search+".json", "w") as outfile:
            json.dump(data, outfile)
        exit()


else:
    pass

#connecting to flipkart 
flipkart_url= 'https://www.flipkart.com/search?q='
uclient= requests.get(flipkart_url+search)

flipkart_html= bs(uclient.content, 'html.parser')
product_= flipkart_html.find_all('div', {'class':"_2kHMtA"})

url= 'https://www.flipkart.com'

#getting the link of exact product
for i in product_:
    new_product_link= url+i.find('a')['href']

#connecting to exact product page
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

#fetching all the data of parent class and running a for loop and providing the child class 
#as all the reviews are their in the child class 
reviewboxes= item_html.find_all('div', {'class':"_16PBlm"})

for i in reviewboxes:
    reviews= i.find('div', {'class': 't-ZTKy'})
    
    if reviews is not None:
        item_reviews.append(reviews.text)

    else:
        item_reviews.append('N/A')


mydict= {'_id': srch,'Name': item_name, 'Price': item_price, 'Ratings': item_rating, 'Specifications': item_specs, 'Review': item_reviews}

with open('Scrapped data/'+search+".json", "w") as outfile:
    json.dump(mydict, outfile)

#Dumping data to the database
add_data= collection.insert_one(mydict)
print('Data sucessfully added to the database')


### Code By:
### Aman Kumar













