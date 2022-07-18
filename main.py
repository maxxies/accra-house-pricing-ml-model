from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
import math
from geopy.geocoders import Nominatim
import pickle
import warnings
import numpy as np
import pandas as pd

app = FastAPI()

templates = Jinja2Templates(directory="deployment/templates")
app.mount("/static", StaticFiles(directory="deployment/static"), name="static")

loaded_model = pickle.load(open("deployment/model.pkl", "rb"))
loaded_encoder = pickle.load(open("deployment/encoder.pickle", "rb"))

# Predicts price with user data
def PricePredictor(location,to_predict_list):
    userData={"Location" :[location]}
    data = pd.DataFrame(userData)
    enc=loaded_encoder.transform(data[["Location"]]).toarray()
    new_array = np.concatenate([to_predict_list,enc[0]]).reshape(1,230)
    result = loaded_model.predict(new_array)
    return abs(result[0])


@app.get('/', response_class=HTMLResponse)
def start_app(request: Request):
    prediction = None
    error = None
    return templates.TemplateResponse("index.html", {"request":request, "prediction":prediction, "error":error})


@app.post('/', response_class=HTMLResponse)
def predict(request: Request, location: str = Form(...), bathrooms: int = Form(...), bedrooms: int = Form(...), garages: int = Form(...)):
    prediction = None
    error = None

    location = location
    bathroom = bathrooms
    bedroom = bedrooms
    garage = garages

    # cleans location input by user
    if ',' in location:
        end = location.index(',')
    else:
        end = None
    location = "".join(location[: end])  # takes name from list by slicing
    if location.lower() == "dome":  # To distinguish among Benin's and Ghana's
        location = location + ',Ghana'

    try:
        # Gets longitude and latitude from location entered
        geolocator = Nominatim(user_agent="maxmawube@gmail.com")
        location_coordinates = geolocator.geocode(location)
        latitude = location_coordinates.latitude
        longitude = location_coordinates.longitude
    except:
        latitude = None
        longitude = None

    # checks if coordinates were received
    if latitude is None and longitude is None:
        return templates.TemplateResponse('index.html', {"request":request, "prediction":prediction,
                                   "error":"Could not get coordinates of location, no or weak connection."})
    # Checks if locations are found in Accra only
    elif math.floor(latitude) != 5:
        return templates.TemplateResponse('index.html',{"request":request, "prediction":prediction,
                                   "error":"Location not found in Accra."})
    # When no error is encountered
    else:
        # Making predictions : latitude,longitude, bedrooms, garage, bathroom
        predictprice = PricePredictor(location,[latitude, longitude, int(bedroom), int(garage), int(bathroom)])
        warnings.filterwarnings("ignore")
        prediction = "{0:,.2f}".format(predictprice)

        return templates.TemplateResponse('index.html', {"request":request, "prediction":prediction, "error":error})


if __name__ == '__main__':
    uvicorn.run(app)
