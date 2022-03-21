from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service


PATH = "C:\programs\chromedriver.exe"
ser = Service(PATH)
op = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=ser, options= op)

driver.get("https://meqasa.com/houses-for-sale-in-Accra.html?w=1")
count = 1

try:
    datacontainer = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.ID,"listview")))
    databox = datacontainer.find_element(By.CLASS_NAME("row.mqs-featured-prop-inner-wrap.clickable"))

# source = requests.get("https://meqasa.com/houses-for-sale-in-Accra.html?w=4").text
# soup = BeautifulSoup(source, 'lxml')
# # Scraping all html tags with data needed
    for data in databox:
        inner_li_shower = data.find_element(By.CLASS_NAME('shower'))       # bathroom tag data
        inner_li_bed = data.find_element(By.CLASS_NAME('bed'))                # bed tag data
        inner_li_garage = data.find_element(By.CLASS_NAME('garage'))            # garage tag data
        price_data = data.find_element(By.CLASS_NAME('h3')).text                 # price data tag
        loc_data = data.find_element(By.CLASS_NAME('h2')).text
        # checking if bathroom data is available before scraping number
        if inner_li_shower is not None:
            bathrooms = inner_li_shower.find_element(By.TAG_NAME("span")).text
        else:
            bathrooms = None

        # checking if bed data is available before scraping number
        if inner_li_bed is not None:
            bedrooms = inner_li_bed.find_element(By.TAG_NAME("span")).text
        else:
            bedrooms = None

         # checking if garage data is available before scraping number
        if inner_li_garage is not None:
            garage = inner_li_garage.find_element(By.TAG_NAME("span")).getText()
        else:
            garage = None

        # slicing actual price from scraped price data
        if price_data is not None:
            main_price = "".join(price_data[9:].split(',')).strip()         # Splitting price from string
            # checks if splitted price is a number or string
            if main_price.isdigit():
                price = int(main_price)
            else:
                price = None
        else:
            price = None

        # slicing actual location from scraped location data
        if loc_data is not None:
            loc = loc_data.findElement(By.TAG_NAME("a")).text                      # converts location data to list of items
            location = " ".join(loc[loc.index('at') + 1:None])    # takes name from list by slicing list
        else:
            location = None

        print("Location :", location)
        print('bathrooms :', bathrooms)
        print('bedrooms :', bedrooms)
        print('garage :', garage)
        print('Price :',price)
        count += 1

finally:
    driver.quit()
# print(count)
# print(soup.prettify())