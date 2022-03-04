from bs4 import BeautifulSoup
import requests

source = requests.get("https://meqasa.com/houses-for-sale-in-Accra.html?w=1").text
soup = BeautifulSoup(source, 'lxml')

count = 1
# Scraping all html tags with data needed
for data in soup.find_all('div', class_='mqs-prop-dt-wrapper'):
    inner_li_shower = data.find('li',class_='shower')             # bathrooms tag data
    inner_li_bed = data.find('li', class_='bed')                  # bed tag data
    inner_li_garage = data.find('li',class_='garage')             # garage tag data
    price_data = data.find('p',class_='h3')                       # price data tag

    # checking if bathroom data is available before scraping number
    if inner_li_shower is not None:
        bathrooms = inner_li_shower.span.text
    else:
        bathrooms = None

        # checking if bed data is available before scraping number
        if inner_li_bed is not None:
            bedrooms = inner_li_bed.span.text
        else:
            bedrooms = None

     # checking if garage data is available before scraping number
    if inner_li_garage is not None:
        garage = inner_li_garage.span.text
    else:
        garage = None
#
    if price_data is not None:
        price = price_data.text
    else:
        price = None

#     # slicing actual location from scraped location data
    if data.h2.a is not None:
        loc = data.h2.a.text.split()               # converts location data to list of items
        location = " ".join(loc[loc.index('at') + 1:None])    # takes name from list by slicing list
    else:
        location = None

    print("Location :", location)
    print('bathrooms :', bathrooms)
    print('bedrooms :', bedrooms)
    print('garage :', garage)
    print('Price :',price)
    count += 1
print(count)
# loc = '4 bedroom House for sale at Adenta Frafraha'.split()
# print(" ".join(loc[loc.index('at')+1:None]))
print(soup.prettify())