from bs4 import BeautifulSoup
import requests

source = requests.get("https://meqasa.com/houses-for-sale-in-Accra.html?w=4").text
soup = BeautifulSoup(source, 'lxml')
count = 1
# Scraping all html tags with data needed
for data in soup.find_all('div', class_='mqs-prop-dt-wrapper'):
    inner_li_shower = data.find('li',class_='shower')             # bathroom tag data
    inner_li_bed = data.find('li', class_='bed')                  # bed tag data
    inner_li_garage = data.find('li',class_='garage')             # garage tag data
    price_data = data.find('p',class_='h3')                       # price data tag
    loc_data = data.find('h2')
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

    # slicing actual price from scraped price data
    if price_data is not None:
        main_price = "".join(price_data.text[9:].split(',')).strip()         # Splitting price from string
        # checks if splitted price is a number or string
        if main_price.isdigit():
            price = int(main_price)
        else:
            price = None
    else:
        price = None

    # slicing actual location from scraped location data
    if loc_data is not None:
        loc = loc_data.a.text.split()                          # converts location data to list of items
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
# print(soup.prettify())