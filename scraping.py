from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from geopy.geocoders import Nominatim

# Driver settings
PATH = "C:\programs\chromedriver.exe"
ser = Service(PATH)
op = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=ser, options= op)
driver.get("https://meqasa.com/houses-for-sale-in-Accra.html?w=1")     # Url of page to be scrapped

count = 1

# Scraping data
try:
    page_count = 1
    while page_count < 2:
        # Scrapes container from which data is found.(container--> HTML element data is in)
        datacontainer = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'pg'+str(page_count))))
        # Gets all the data from the container
        databox = datacontainer.find_elements(By.CLASS_NAME, 'row.mqs-featured-prop-inner-wrap.clickable')

        #   Loops through list of data to scrap specific data-information from a data taken at a time
        for data in databox:
            # Scraping the number of shower from a single data
            try:
                li_shower = data.find_element(By.CLASS_NAME,'shower')
                inner_li_shower = li_shower.find_element(By.TAG_NAME,'span').get_attribute("innerHTML")
            except NoSuchElementException:
                # Sets none when no shower-data is found for a particular data
                inner_li_shower = None

            # Scraping he number of bed spaces give data
            try:
                li_bed = data.find_element(By.CLASS_NAME,'bed')
                inner_li_bed = li_bed.find_element(By.TAG_NAME,'span').get_attribute("innerHTML")
            except NoSuchElementException:
                # Sets none when no bed-data is found for a particular data
                inner_li_bed = None

            # Scraping number of garage
            try:
                li_garage = data.find_element(By.CLASS_NAME,'garage')
                inner_li_garage = li_garage.find_element(By.TAG_NAME,'span').get_attribute("innerHTML")
            except NoSuchElementException:
                # Sets none when no garage-data is found for a particular data
                inner_li_garage = None

            # Scraping price
            try:
                price_data = data.find_element(By.CLASS_NAME, 'h3').get_attribute("innerText")
                # Splitting price from string
                price_data = str(price_data)
                main_price = "".join(price_data[3:].split(',')).strip()
                # checks if splitted price is a number or string
                if main_price.isdigit():
                    price = int(main_price)
                else:
                    price = None
            except :
                price = None

            # Breaks out out scraping particular data when no price is given
            if price == None:
                break

            # Scraping location
            loc_box = data.find_element(By.TAG_NAME,'h2')
            loc_data = loc_box.find_element(By.TAG_NAME,'a').get_attribute("innerHTML")

            # slicing actual location from scraped location data
            """
                Most locations have Hills attached to them which gives the wrong coordinates thus, the need to remove them.
            """
            if 'hills' in loc_data and ',' in loc_data:
                hills_loc = loc_data.index('hills')
                comma_loc = loc_data.index(',')
                end = min(hills_loc, comma_loc)
            elif ',' in loc_data and 'hills' not in loc_data:
                end = loc_data.index(',')
            elif 'hills' in loc_data and ',' not in loc_data:
                end = loc_data.index('hills')
            else:
                end = None
            location = "".join(loc_data[loc_data.index('at') + 3: end])  # takes name from list by slicing

            # Getting latitudes and longitudes of location
            try:
                geolocator = Nominatim(user_agent="https")
                location_coordinates = geolocator.geocode(location)
                latitude = location_coordinates.latitude
                longitude = location_coordinates.longitude
            except AttributeError:
                latitude = None
                longitude = None
            print("----------------------------------->>>", count)
            print("Location :", location)
            print("Latitudes :", latitude)
            print("Longitudes :", longitude)
            print("Shower :",inner_li_shower)
            print("Bed :",inner_li_bed)
            print("Garage :",inner_li_garage)
            print('Price :',price)
            count += 1

        count = 1
        button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "pagenumnext")))
        button.click()
        page_count = page_count + 1

except TimeoutException :
    print("TIme out error.")
    driver.close()
finally:
    driver.quit()
# print(count)
# print(soup.prettify())