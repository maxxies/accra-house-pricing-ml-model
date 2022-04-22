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
This a machine learning model centered on predicting house prices in Accra. This is deployed using a web framework for user interaction with the model. The model makes use of data from a trusted source.
## Sections

### Overview
- Building the the predictor makes use of many processes or actions which would be talked about. These have been worked out in different files as seen above.
### Data
- The data used for this project was scrapped from a trusted website, [meqasa.com](https://meqasa.com/houses-for-sale-in-Accra.html?w=1).
- Selenium and BeautifulSoup were options to be used for the scraping but due to the nature of the website, selenium was used.
- Selenium offered web interactions which helped in scrapping the data unlike BeautifulSoup.
- Illustrations on using both libraries for scraping the website has been done.
- The data comprises of :
     - Location of the house
     - Number of available bedrooms
     - Number of available bathrooms
     - Number of available garages
- Additional information like the longitude and latitude of the location of the house was added to the data with the help of a library in python.
- Data was cleaned and fed to the model.
### Model
- Consideration were made on predictors like Linear Regression, Decision Tree Regressor, Random Forest Regressor and Support Vector Regressor(SVR). 
- After data was split into the train, test and validation sets, they were tested against all these predictors to get the one that works best on them.
- The model was then built on the chosen predictor after finding the best parameters for it.
- The model was then saved to be used by the flask app.
### Deployment
- The interface that was used to serve the model to users is a web app built with Flask.
- The saved model is used up in the app to predict for data inputted by users.
