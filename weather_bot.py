import tweepy
import requests
import os
import datetime
import random
from dotenv import load_dotenv
from time import sleep
from apscheduler.schedulers.blocking import BlockingScheduler

load_dotenv()
base_url = "http://api.openweathermap.org/data/2.5/weather?"
#city = "Hamilton"
new_jersey_cities = ['Edison','Hamilton','New Brunswick','Jersey City','Newark','Trenton'
                     ,'Princeton','Paterson','Toms River','Hoboken',
                     'Cherry Hill','Hackensack','Bayonne','Passaic','Plainfield','Piscataway','East Brunswick','East Orange',
                     'Secaucus','Long Branch','Old Bridge', 'Monroe Township','Red Bank', 'Perth Amboy',
                     'Holmdel', 'Bergenfield','Atlantic City','Sayreville']

city_today = random.choice(new_jersey_cities)
weather_key = os.environ.get("weather_key")
url = base_url + "appid=" + weather_key + "&q=" + city_today
all_weather_data = requests.get(url).json()

def kelvin_to_fahrenheit(kelvin):
    degrees_fahrenheit = ((kelvin - 273.15) * (9/5) + 32)
    return degrees_fahrenheit

#current_time = datetime.datetime.now().strftime("%H:%M:%S")
temp_in_fahrenheit = kelvin_to_fahrenheit(all_weather_data['main']['temp'])
feels_temp = kelvin_to_fahrenheit(all_weather_data['main']['feels_like'])
wind_speed = all_weather_data['wind']['speed']
humidity = all_weather_data['main']['humidity']
desc = all_weather_data['weather'][0]['description']
sunrise = datetime.datetime.utcfromtimestamp(all_weather_data['sys']['sunrise'] + all_weather_data['timezone']).strftime("%H:%M:%S")
sunset = datetime.datetime.utcfromtimestamp(all_weather_data['sys']['sunset'] + all_weather_data['timezone']).strftime("%H:%M:%S")

tweet_starter_words = ['Care to see the weather?','Weather time!!!!','Time to view the weather!','Here is your automated weather report!']

starter_word = random.choice(tweet_starter_words)

bot_message = f"""{starter_word} The sun rises today in {city_today} at {sunrise} and sets at {sunset} local time. 
The current temperature is {round(temp_in_fahrenheit)}°F but it feels like {round(feels_temp)}°F! Morning conditions are {desc}...
Winds speeds are at {wind_speed} m/s and the humidity right now is {humidity}%. """

api_key = os.environ.get("twitter_api_key")
api_secret = os.environ.get("twitter_api_secret")
access_token = os.environ.get("twitter_access_token")
access_token_secret = os.environ.get("twitter_access_token_secret")
bearer_token = os.environ.get("twitter_bearer_token")


client = tweepy.Client(
    bearer_token,
    api_key,
    api_secret,
    access_token,
    access_token_secret,
    wait_on_rate_limit = True
)

def send_tweet():
    client.create_tweet(text=bot_message)
send_tweet()



