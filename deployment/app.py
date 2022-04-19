from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/', methods=['GET'])
def start_app():
    return render_template('index.html')


@app.route('/', methods=['POST', 'GET'])
def predict():

    if request.method == 'POST':
        location = request.form['location']
        bathroom = request.form['bathrooms']
        bedroom = request.form['bedrooms']
        garage = request.form['garages']

        return render_template('index.html', data = location, one = bathroom, two = bedroom, three= garage)
    else:
        return render_template('index.html')


if __name__ == '__main__':
    app.run(port=3000, debug=True)
