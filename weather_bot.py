import tweepy
import requests
import os
import datetime
import random
import pandas as pd
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import logging

#load .env to get api keys
load_dotenv()

#set up logging for print/debug statements
logging.basicConfig(level=logging.INFO)

#define constants
KELVIN_TO_FAHRENHEIT_CONSTANT = 273.15
TWEET_CHARACTER_LIMIT = 280

#retrieve API keys
weather_key = os.getenv("weather_key")
api_key = os.getenv("twitter_api_key")
api_secret = os.getenv("twitter_api_secret")
access_token = os.getenv("twitter_access_token")
access_token_secret = os.getenv("twitter_access_token_secret")
bearer_token = os.getenv("twitter_bearer_token")

#weather API setup
base_url = "http://api.openweathermap.org/data/2.5/weather?"
#list all 52 NJ cities 

new_jersey_cities = [
    "Absecon","Asbury Park","Atlantic City","Bayonne","Bergenfield","Bloomfield",
    "Camden","Cape May","Cherry Hill","Clifton","East Orange","Edison","Elizabeth","Englewood","Ewing",
    "Fort Lee","Franklin","Garfield","Glassboro","Hackensack","Hoboken","Irvington","Jersey City",
    "Linden","Long Branch","Marlboro","Middletown","Newark","North Bergen","Parsippany-Troy Hills",
    "Perth Amboy","Phillipsburg","Plainfield","Princeton","Rahway","Randolph","Red Bank","Ridgewood",
    "Roselle","Sayreville","Somerville","Teaneck","Trenton","Union City","Vineland","West New York","West Orange","Woodbridge",
    "East Brunswick","Mount Laurel","North Brunswick"
]

#get num of cities total for reference
# print(len(new_jersey_cities))

#setup twitter API client (V1)
auth = tweepy.OAuthHandler(api_key, api_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit = True)

#setup twitter API client (V2)
client = tweepy.Client(
    bearer_token,
    api_key,
    api_secret,
    access_token,
    access_token_secret,
    wait_on_rate_limit=True
)

#function to retrieve weather data from 
def get_weather_data(city):
    url = base_url + "appid=" + weather_key + "&q=" + city
    try:
        all_weather_data = requests.get(url).json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching data for {city}: {e}")
        return None

    if all_weather_data.get('main') and all_weather_data.get('wind') and all_weather_data.get('weather'):
        temp_in_fahrenheit = kelvin_to_fahrenheit(all_weather_data['main']['temp'])
        feels_temp = kelvin_to_fahrenheit(all_weather_data['main']['feels_like'])
        wind_speed = all_weather_data['wind']['speed']
        humidity = all_weather_data['main']['humidity']
        desc = all_weather_data['weather'][0]['description']
        sunrise = datetime.datetime.utcfromtimestamp(all_weather_data['sys']['sunrise'] + all_weather_data['timezone']).strftime("%H:%M:%S")
        sunset = datetime.datetime.utcfromtimestamp(all_weather_data['sys']['sunset'] + all_weather_data['timezone']).strftime("%H:%M:%S")

        return {
            "city": city,
            "temp": temp_in_fahrenheit,
            "feels_like": feels_temp,
            "wind_speed": wind_speed,
            "humidity": humidity,
            "description": desc,
            "sunrise": sunrise,
            "sunset": sunset,
            "timestamp": datetime.datetime.now()
        }
    else:
        return None

#convert kelvin to F
def kelvin_to_fahrenheit(kelvin):
    return ((kelvin - KELVIN_TO_FAHRENHEIT_CONSTANT) * (9/5)) + 32

#function to send a more friendly tweet regarding the day's weather
def daily_weather_tweet():
    city_today = random.choice(new_jersey_cities)
    weather_data = get_weather_data(city_today)

    if weather_data:
        tweet_starter_words = ['Care to see the weather?', 'Weather time!', 'Here is your weather report!']
        starter_word = random.choice(tweet_starter_words)
        bot_message = f"""{starter_word} The sun rises today in {city_today} at {weather_data['sunrise']} and sets at {weather_data['sunset']} local time. 
        The current temperature is {round(weather_data['temp'])}°F but it feels like {round(weather_data['feels_like'])}°F! 
        Winds are at {weather_data['wind_speed']} m/s, and the humidity is {weather_data['humidity']}%. Conditions: {weather_data['description']}."""

        if len(bot_message) <= TWEET_CHARACTER_LIMIT:
            client.create_tweet(text=bot_message)
            logging.info("Tweet sent successfully")
        else:
            logging.warning("Tweet exceeds character limit!")
    else:
        logging.error("Error fetching weather data")

#function to collect weather data for all cities, and store them in a csv
def collect_weather_data():
    data = []
    for city in new_jersey_cities:
        weather_data = get_weather_data(city)
        if weather_data:
            data.append(weather_data)
    
    # Save the data as a CSV
    df = pd.DataFrame(data)
    df.to_csv('weather_data.csv', index=False)
    logging.info("Weather data collected and saved")


#function to perform an analysis and tweet summary with a graph of high temperatures
def analysis():
    df = pd.read_csv('weather_data.csv')

    #get statistics
    avg_temp = df['temp'].mean()
    max_temp = df['temp'].max()
    min_temp = df['temp'].min()
    temp_range = max_temp - min_temp
    avg_humidity = df['humidity'].mean()
    avg_wind_speed = df['wind_speed'].mean()
    most_common_desc = df['description'].mode()[0]
    total_records = df.shape[0]  # Total records for percentage calculation

    today = datetime.date.today()
    formatted_date = today.strftime("%m/%d/%Y")
    
    #create our message string
    tweet_message = (
        f"Daily Weather Analysis for NJ Cities({formatted_date}):\n"
        f"Average Temperature: {round(avg_temp)}°F\n"
        f"Max Temperature: {round(max_temp)}°F\n"
        f"Min Temperature: {round(min_temp)}°F\n"
        f"Temperature Range: {temp_range:.2f}°F\n"  #need to format with 2 decimal places for some reason
        f"Average Humidity: {round(avg_humidity)}%\n"
        f"Average Wind Speed: {round(avg_wind_speed, 2)} m/s\n"
        f"Most Common Weather Condition: {most_common_desc}\n"
        f"Total Cities Analyzed: {total_records}"
    )

    #get only the top 30 hottest cities for our graph
    top_cities = df.nlargest(30, 'temp')

    #create a bar graph of high temperatures for the top 30 cities
    plt.figure(figsize=(14, 8))
    colors = ['red'] * 8 + ['lightcoral'] * 8 + ['orange'] * 8 + ['yellow'] * 6 #use different colors for the temperatures
    plt.bar(top_cities['city'], top_cities['temp'], color=colors)
    #x,y and title labels
    plt.xlabel('City')
    plt.ylabel('High Temperature (°F)') 
    plt.title('30 Hottest NJ Cities Today')

    #adjust x-ticks to show all cities with smaller font size and angle
    plt.xticks(rotation=45, ha='right', fontsize=8)

    #set x-ticks to ensure all cities are displayed
    plt.gca().set_xticks(range(len(top_cities)))
    plt.gca().set_xticklabels(top_cities['city'], rotation=45, ha='right', fontsize=8)

    #adjust y-ticks to go by 5's
    plt.yticks(range(0, int(max(top_cities['temp'])) + 5, 5))

    #set y-ticks to be more frequent
    plt.gca().yaxis.set_major_locator(plt.MaxNLocator(integer=True, prune='both'))

    plt.tight_layout()  #use tight layout

    #save the plot as an png image
    image_path = 'hottest_nj_cities.png'
    plt.savefig(image_path)
    plt.close()

    #check that tweet message is within Twitter's character limit
    if len(tweet_message) <= 280:
        # Upload image and tweet
        media_id = api.media_upload(filename=image_path).media_id_string
        client.create_tweet(text=tweet_message, media_ids=[media_id])
        logging.info("Analysis + image tweeted succesfully ")
    else:
        logging.warning("Cannot tweet as it exceeds limit!")


# uncomment 1 for friendly report, uncomment 2&3 for anaylsis report 
#(1) daily_weather_tweet()  
#(2)collect_weather_data()  
#(3) analysis()
