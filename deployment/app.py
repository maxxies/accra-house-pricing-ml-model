import math

from flask import Flask, render_template, request
from geopy.geocoders import Nominatim

app = Flask(__name__)


@app.route('/', methods=['GET'])
def start_app():
    location = None
    bathroom = None
    bedroom = None
    garage = None
    prediction = None
    error = None

    return render_template('index.html', data=location, one=bathroom, two=bedroom, three=garage, prediction=error,
                           error=error)


@app.route('/', methods=['POST'])
def predict():
    location = None
    bathroom = None
    bedroom = None
    garage = None
    latitude = None
    longitude = None

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
            geolocator = Nominatim(user_agent="accrahousepricing")
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
            prediction = 20236699
            return render_template('index.html', data=location, send=send, one=bathroom, two=bedroom, three=garage,
                                   latitude=latitude, longitude=longitude, prediction=prediction, error=error)

    else:
        return render_template('index.html', data=location, one=bathroom, two=bedroom, three=garage,
                               prediction=prediction,
                               error=error)


if __name__ == '__main__':
    app.run(port=3000, debug=True)