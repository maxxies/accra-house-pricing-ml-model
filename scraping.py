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
from geopy.extra.rate_limiter import  RateLimiter
import csv
import time
import math

# Driver settings
PATH = "C:\programs\chromedriver.exe"
ser = Service(PATH)
op = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=ser, options= op)
driver.get("https://meqasa.com/houses-for-sale-in-Accra.html?w=1")     # Url of page to be scrapped

count = 1
total_count = 0
# Scraping data
try:
    # Setting up csv file to write data into to csv file
    csv_file = open('housing_data.csv', 'a', newline='')
    csv_writer = csv.writer(csv_file, delimiter=',')
    csv_writer.writerow(['Location', 'Latitude', 'Longitude', 'Bedrooms', 'Bathrooms', 'Garage', 'Price'])
    page_count = 1
    while page_count < 716:
        # Scrapes container from which data is found.(container--> HTML element data is in)
        datacontainer = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'pg'+str(page_count))))
        # Gets all the data from the container
        databox = datacontainer.find_elements(By.CLASS_NAME, 'row.mqs-featured-prop-inner-wrap.clickable')

        #   Loops through list of data to scrap specific data-information from a data taken at a time
        for data in databox:
            # Scraping the number of bathrooms
            try:
                li_shower = data.find_element(By.CLASS_NAME,'shower')
                inner_li_shower = li_shower.find_element(By.TAG_NAME,'span').get_attribute("innerHTML")
            except NoSuchElementException:
                # Sets none when no shower-data is found for a particular data
                inner_li_shower = None

            # Scraping the number of bed spaces
            try:
                li_bed = data.find_element(By.CLASS_NAME,'bed')
                inner_li_bed = li_bed.find_element(By.TAG_NAME,'span').get_attribute("innerHTML")
            except NoSuchElementException:
                # Sets none when no bed-data is found for a particular data
                inner_li_bed = None

            # Scraping number of garage spaces
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
                # checks if price is a number or string
                if main_price.isdigit():
                    price = main_price
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
            if ',' in loc_data:
                end = loc_data.index(',')
            else:
                end = None
            location = "".join(loc_data[loc_data.index('at') + 3: end])  # takes name from list by slicing
            if location.lower() == "dome":   # To distinguish among Benin's and Ghana's
                location = location + ',Ghana'

            # Getting latitudes and longitudes of location
            time.sleep(2)
            try:
                geolocator = Nominatim(user_agent="ahiamadzormaxwell7@gmail.com")
                geocode = RateLimiter(geolocator.geocode, min_delay_seconds=2)
                location_coordinates = geocode(location)
                latitude = location_coordinates.latitude
                longitude = location_coordinates.longitude
            except :
                latitude = None
                longitude = None



            # Writing processed scraped data to csv file
            if price is not None and latitude is not None and longitude is not None :     # Allow only data with price, lonitude and latitude values
                if math.floor(latitude) == 5:
                    if location.lower() == "dome,ghana":  # To change name back to Dome
                        location = 'Dome'
                    # Checks if town is around accra based on latitude
                    csv_writer.writerow([location.lower().capitalize(), float(latitude), float(longitude), int(inner_li_bed), int(inner_li_shower), int(inner_li_shower), int(price)])
                    count += 1
            total_count += 1

        # Clicks on button to load next page data
        button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "pagenumnext")))
        button.click()
        page_count = page_count + 1

except TimeoutException :
    print("TIme out error.")
    driver.close()
    csv_file.close()
finally:
    driver.quit()
    csv_file.close()
    print("Total Pages:", page_count)
    print("Total Data: ", total_count)
    print("Saved Data: ", count)