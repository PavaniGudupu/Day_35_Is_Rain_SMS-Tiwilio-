import os
import requests
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient

OWN_Endpoint = "https://api.openweathermap.org/data/2.5/forecast"
api_key = "b95b252a0b39358f5e1d33f54a87c407"


account_sid = "AC9ea758c035b6d5b78b63306803b77d5d"
auth_token = "5761b6725d4694563a7c7a0dddbc4fc0"



weather_params = {
    "lat": 51.5074,
    "lon": -0.1278,
    "appid": api_key,
    "cnt": 4,
}

response = requests.get(OWN_Endpoint, params=weather_params)
response.raise_for_status()
weather_data = response.json()

will_rain = False
for hour_data in weather_data["list"]:
    condition_code = hour_data["weather"][0]["id"]
    if int(condition_code) < 700:
        will_rain = True

if will_rain:
    proxy_client = TwilioHttpClient()
    proxy_client.session.proxies = {'https': os.environ['https_proxy']}
    
    client = Client(account_sid, auth_token, http_client=proxy_client)
    message = client.messages.create(
        body="🌧️ Looks like it's going to rain today! Don't forget to grab your umbrella ☔️ and stay dry. Have a great day! 😊",
        from_="+12512377378",  # Your Twilio number
        to="+917995058698",    # The recipient's number in E.164 format
    )

    print(message.status)
    print("RAINING")

else:
    print("No raining...")