# accra-house-pricing-ml-model
A machine learning model to predict the price of a house in Accra, Ghana when given the location, number of bedroomws, number of bathrooms and number of garages.
## Table of Contents

* [Overview](#overview)
* [Sections](#sections)
    * [Overview](#overview)
    * [Data](#data)
    * [Model](#model)    
    * [Deployment](#deployment)
    
## Overview
This a machine learning model centered on predicting hose prices in Accra. This is deployed using a web framework for user interaction with the model.Th e model make use data from a trusted source.
## Sections

### Overview
- Building the the predictor makes use of many processes or actions which would be talked about.
### Data
- The data used for the model was scrapped from a trusted website, [meqasa.com](https://meqasa.com/houses-for-sale-in-Accra.html?w=1).
- Selenium and BeautifulSoup were options to be used for the scraping but due to the nature of the website, selenium was used.
- Selenium offered web interactions which helped in scrapping the data unlike BeautifulSoup.
- The data comprises of :
     - Location of the house
     - Number of available bedrooms
     - Number of available bathrooms
     - Number of available garages
- Additional information like the longitude and latitude of the location of the house was added to the data with the help of a library in python.
- Data was cleaned and fed to the model.
### Model
### Deployment
