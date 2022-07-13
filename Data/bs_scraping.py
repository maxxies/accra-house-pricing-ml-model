from bs4 import BeautifulSoup
import requests

source = requests.get("https://meqasa.com/houses-for-sale-in-Accra.html?w=1").text
soup = BeautifulSoup(source, 'lxml')

main_data_container = soup.find("div", id='pg1')
count = 1
print(main_data_container)
for data in main_data_container.find_all('div', class_="row mqs-featured-prop-inner-wrap clickable"):
    print(count)

    data_box = data.find('div',class_="mqs-prop-dt-wrapper")
    location_box = data_box.find('h2')
    shower_container = data_box.find('li', class_="shower")
    bed_container = data_box.find('li', class_="bed")
    garage_container = data_box.find('li', class_="garage")
    price_data = data_box.find('p', class_='h3')

    shower = shower_container.span.text if shower_container else None
    bed = bed_container.span.text if bed_container else None
    garage = garage_container.span.text if garage_container else None
    location = location_box.text if location_box else None
    price = price_data.text if price_data else None

    print("Location :", location)
    print("Price :", price)
    print("Garage :", garage)
    print('Bed :',bed)
    print("Location :", location)
    print("Bathrooms :", shower)
    count = count + 1
print("Data")
