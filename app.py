import requests
import json
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask("Weather App")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///product.sqlite3'
db = SQLAlchemy(app)


lat = 27.7172
longi = 85.3240
@app.route('/')
def home():
    url = 'https://api.open-meteo.com/v1/forecast?latitude=%f&longitude=%f&current_weather=true' % (
        lat, longi)
    r = requests.get(url).text
    response = json.loads(r)
    # print(r)
    # print(url)
    return render_template("index.html", test=response)


@app.route('/locate', methods=['POST', 'GET'])
def locate():
    url = "https://geocode.maps.co/search?q="
    if request.method == 'POST':
        location = request.form['location']
        location = location.strip()
        if (location != ''):
            r = requests.get(url=url+"{"+location+"}")
            data = r.json()
            lat = float(data[0]['lat'])
            longi = float(data[0]['lon'])
            place = data[0]["display_name"]
            place = (place.split())[0] + (place.split(","))[-1]
        return(located(lat, longi, place))

def located(lat, longi, place):
    url = 'https://api.open-meteo.com/v1/forecast?latitude=%f&longitude=%f&current_weather=true' % (
        lat, longi)
    r = requests.get(url).text
    response = json.loads(r)
    # print(r)
    # print(url)
    return render_template("located.html", test=response, location = place)
