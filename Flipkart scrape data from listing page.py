import requests
from urllib.request import urlopen as ureq
from bs4 import BeautifulSoup as bs
import pandas as pd

srch= input('Enter the product name: ')
search= srch.replace(' ','')

flipkart_url= 'https://www.flipkart.com/search?q='
uclient= requests.get(flipkart_url+search)
#page_html= uclient.read()
#uclient.close()
flipkart_html= bs(uclient.content, 'html.parser')

product_= flipkart_html.find_all('div', {'class':"_2kHMtA"})


item_name= []
item_ratings = []
item_price= []
item_specs= []
item_link= []

url= 'https://www.flipkart.com'

for item in product_:
    name= item.find('div',attrs={'class': '_4rR01T'})
    item_name.append(name.text)
    specs= item.find('div', attrs={'class': 'fMghEO'})
    item_specs.append(specs.text)
    ratings= item.find('div',attrs= {'class':"_3LWZlK"})
    if ratings is not None:
        item_ratings.append(ratings.text)
    else:
        item_ratings.append('Not Rated Yet')
    price= item.find('div', {'class':'_30jeq3 _1_WHN1'}).text
    item_price.append(price)
    ilink= url+item.find('a')['href']
    item_link.append(ilink)

print(len(item_name))
print(len(item_ratings))
print(len(item_specs))
print(len(item_link))
print(len(item_price))


mydict= {'Product Name': item_name, 'Price': item_price, 'Ratings': item_ratings, 'Specifications': item_specs, "Item Link": item_link}
df=pd.DataFrame(mydict)
df.to_csv('Scrapped data/'+srch+'.csv')







