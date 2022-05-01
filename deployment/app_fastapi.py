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

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

model = pickle.load(open("model_rf.pkl", "rb"))


def price_predictor(to_predict_list):
    to_predict = np.array(to_predict_list).reshape(1, 5)
    result = model.predict(to_predict)
    return result[0]


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
        predictprice = price_predictor([latitude, longitude, int(bedroom), int(garage), int(bathroom)])
        warnings.filterwarnings("ignore")
        prediction = "{0:,.2f}".format(predictprice)

        return templates.TemplateResponse('index.html', {"request":request, "prediction":prediction, "error":error})


if __name__ == '__main__':
    uvicorn.run(app)
