import math
from flask import Flask, render_template, request
from geopy.geocoders import Nominatim
import pickle
import warnings
import numpy as np

app = Flask(__name__)

model = pickle.load(open("model_rf.pkl", "rb"))


def price_predictor(to_predict_list):
    to_predict = np.array(to_predict_list).reshape(1, 5)
    result = model.predict(to_predict)
    return result[0]


@app.route('/', methods=['GET'])
def start_app():
    prediction = None
    error = None

    return render_template('index.html', prediction=prediction, error=error)


@app.route('/', methods=['POST'])
def predict():
    prediction = None
    error = None

    if request.method == 'POST':
        location = request.form['location']
        bathroom = request.form['bathrooms']
        bedroom = request.form['bedrooms']
        garage = request.form['garages']

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
            return render_template('index.html', data=location, one=bathroom, two=bedroom, three=garage,
                                   latitude=latitude, longitude=longitude, prediction=prediction,
                                   error="Could not get coordinates of location, no or weak connection.")
        # Checks if locations are found in Accra only
        elif math.floor(latitude) != 5:
            return render_template('index.html', data=location, one=bathroom, two=bedroom, three=garage,
                                   latitude=latitude, longitude=longitude, prediction=prediction,
                                   error="Location not found in Accra.")
        # When no error is encountered
        else:
            # Making predictions : latitude,longitude, bedrooms, garage, bathroom

            predictprice = price_predictor([latitude, longitude, int(bedroom), int(garage), int(bathroom)])
            # warnings.filterwarnings("ignore")
            prediction = "{0:,.2f}".format(predictprice)

            return render_template('index.html', prediction=prediction, error=error)

    else:
        return render_template('index.html', prediction=prediction, error=error)


if __name__ == '__main__':
    app.run(port=3000, debug=True)
