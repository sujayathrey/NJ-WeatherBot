NJ Weather Bot 🌦️
NJ Weather Bot is an automated Twitter bot that provides daily weather updates, summaries, and analysis for 52 cities in New Jersey. By utilizing the OpenWeatherMap API to fetch current weather conditions, the bot gathers and processes weather data to generate insightful tweets and visualizations. This project is designed to showcase skills in data querying through API integration, data parsing and handling with python, and data visualization/analysis. All these elements are combined into one tweet that is automated at the click of a button.

Project Overview
The bot performs three primary functions:
  1. Daily Weather Tweet: A friendly tweet providing key weather stats (temperature, wind speed, humidity, sunrise, sunset) for a random 
     NJ city.
  2. Data Collection: Collects and stores weather data for all 52 NJ cities into a CSV file for further analysis.
  3. Weather Analysis Summary: Analyzes the data across NJ cities, generates summary statistics, and tweets out an analysis report along 
     with multiple visualizations.

     
Features:
  * Weather Updates for NJ Cities: Gathers real-time data on temperature, humidity, wind speed, and conditions for 52 cities in New Jersey.
  * Random City Daily Report: Sends a weather update for a random NJ city with details on current temperature, feels-like temperature, 
  humidity, wind speed, and weather description.
  * Comprehensive Analysis Report: Calculates and tweets summary statistics across all cities (average temperature, highest and lowest 
    temperatures, humidity, and common weather conditions).

Visual Insights: 
Each tweet will generates and tweets four graphs:
  1. Top 30 hottest cities bar chart.
  2. Temperature vs. humidity scatter plot.
  3. Temperature trend across cities line plot.
  4. Weather condition distribution pie chart.

API Usage: 
The bot utilizes two primary APIs:
  1. OpenWeatherMap API: Retrieves weather data for each NJ city.
  2. Twitter API (v1 and v2): Posts tweets with the gathered data, including text summaries and images of graphs.
