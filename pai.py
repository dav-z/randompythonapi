import datetime
from twilio.rest import Client
import urllib.request, json
from darksky import forecast
from datetime import date, timedelta
import requests
from flask import Flask, request
from twilio import twiml
from twilio.twiml.messaging_response import MessagingResponse

## TO RUN:
#### in terminal: python pai.py
#### in another tab: ngrok http 5000

app = Flask(__name__)

@app.route('/sms', methods=['GET', 'POST'])
def sms():
    number = request.form['From']
    message_body = request.form['Body']
    params = {
    'sensor': 'false',
    'address': message_body,
    ## unsafe to store API Key this way, but the repo is private
    'key': 'AIzaSyDWKIU6UoMtxqFFq3R0C8uXAMXTUquwHdM'
    }
    url = 'https://maps.googleapis.com/maps/api/geocode/json'

    ## calls request to get the information given from the url with address and api key
    r = requests.get(url, params = params)

    ## gets the result in json format
    res = r.json()

    ## gets first result returned
    result = res['results'][0]

    ## creates a hashmap
    geodata = dict()

    ## set variables for long and lat
    lat = result['geometry']['location']['lat']
    lon = result['geometry']['location']['lng']
    account_sid = "AC0787ce7bbc2aed7293ae60beee27480d"
    auth_token  = "734e725ff3b749ff21c8ef7a807359af"

    ## Darksky API KEY
    key = "c9e27dbf8ba59e0820e721f9e3e088f7"

    location = forecast(key, lat, lon)

    testmsg = "Today's temperature is {} degrees at {}".format(location.temperature, message_body)

    resp = MessagingResponse()
    resp.message(testmsg)
    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)

