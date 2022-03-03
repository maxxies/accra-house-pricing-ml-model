from bs4 import BeautifulSoup
import requests

source = requests.get("https://www.meqasa.com").text
soup = BeautifulSoup(source, 'lxml')

# Scraping all html tags with data needed
# for data in soup.find_all('div', class_='one-featured-prop'):
#     # price =
#     inner_div = data.find('div')
#     inner_ul = inner_div.find('ul')
#     inner_li_shower = data.find('li',class_='shower')
#     inner_li_bed = data.find('li', class_='bed')
#     inner_li_garage = data.find('li',class_='garage')
#     bathrooms = inner_li_shower.span.text
#     bedrooms = inner_li_bed.span.text
#     garage = inner_li_garage
#     location = data.div.p
#     # bathrooms
#     # bed
#
#     print("Location", location)
#     print('bathrooms', bathrooms)
#     print('bedrooms', bedrooms)
#     print('garage', garage)
print(soup.prettify())