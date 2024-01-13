# Fetches current weather data for the locations in location.properties
# One every 20 minutes is 3 times per hour or 72 times per day
# Times 12 locations is 864 API calls per day.
# The free tier allows 1000 calls per day.
# We can get more by requesting an academic API key.
# Run this script in the background to collect data for 24 hours.


# Standard library imports
import configparser
import csv
import datetime
import json
import logging
import pathlib
import sys
import time
import os

# Third party imports
import dotenv
import requests

# Local import
from utils.util_api import get_api_key
from utils.util_location import get_lat_lon
from utils.util_log import logger
from utils.util_properties import read_property, read_properties_list


def get_data_folder() -> pathlib.Path:
    """Return the path to the data folder."""
    return pathlib.Path(__file__).parent.joinpath("data")


def fetch_weather_data(api_key, coords) -> dict:
    num_days: int = 30
    end_date = datetime.datetime.now()

    # Initialize a dictionary to store the data
    historical_data = {}

    for day in range(num_days):
        # Calculate the date for each day
        query_date = end_date - datetime.timedelta(days=day)

        # Format the date as Unix timestamp
        timestamp = int(query_date.timestamp())

        # Construct the API URL
        API_URL = f"http://api.openweathermap.org/data/2.5/onecall/timemachine?lat={coords['lat']}&lon={coords['lon']}&dt={timestamp}&appid={api_key}"

        # Logging the URL for debugging purposes
        logging.info(f"Fetching data for {query_date.date()}: {API_URL}")

        # Make the API request
        response = requests.get(API_URL)

        # Check if the response is successful
        if response.status_code == 200:
            # Store the data in the dictionary
            historical_data[query_date.date()] = response.json()
        else:
            logging.warning(f"Failed to fetch data for {query_date.date()}")

    return historical_data


def process_location(api_key, location) -> None:
    location_coords = get_lat_lon(location)
    if location_coords is None:
        logger.warning(f"Coordinates for {location} not found.")
        return

    location_fname = location.split(",")[0].strip() + location.split(",")[1].strip()
    logger.info(f"Processing {location_fname}")

    # Fetch historical weather data every 20 minutes
    weather_data = fetch_weather_data(api_key, location_coords)
    logger.info(f"Fetched data for {location_fname}")

    if not weather_data:
        logger.warning(f"No data found for {location}")
    else:
        logger.info(f"Weather data for {location}: {len(weather_data)} records")
        data_folder = get_data_folder()
        data_folder.mkdir(exist_ok=True)  # Ensure the data folder exists
        file_path = data_folder.joinpath(f"weather_{location_fname}.csv")

        # Write current weather data to a CSV file in the data folder
        try:
            with open(file_path, "w", newline="") as f:
                fieldnames = weather_data[0]["daily"][0].keys()
                writer = csv.DictWriter(f, fieldnames=fieldnames)

                # Write the header row
                writer.writeheader()

                # Write the weather data rows
                for day_data in weather_data:
                    for daily_data in day_data["daily"]:
                        writer.writerow(daily_data)
        except Exception as e:
            logger.error(f"Error writing CSV for {location}: {e}")


def fetch_current_weather_data(api_key, coords) -> dict:
    # Construct the API URL for current weather data
    lat = coords[0]
    lon = coords[1]
    API_URL = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}"

    # Logging the URL for debugging purposes
    logging.info(f"Fetching current weather data for: Lat {lat} Lon {lon}")

    # Make the API request
    response = requests.get(API_URL)

    # Check if the response is successful
    if response.status_code == 200:
        return response.json()
    else:
        logging.warning(
            f"Failed to fetch current weather data. Status code: {response.status_code}"
        )
        return None


def process_location_for_current_weather(api_key, location) -> None:
    location_coords = get_lat_lon(location, api_key)
    if location_coords is None:
        logger.warning(f"Coordinates for {location} not found.")
        return

    location_fname = location.replace(",", "").replace(" ", "")
    file_path = get_data_folder().joinpath(f"weather_{location_fname}.json")
    logger.info(f"Processing current weather for {location_fname}")

    # Fetch current weather data
    weather_data = fetch_current_weather_data(api_key, location_coords)

    if weather_data:
        logger.info(f"Weather data for {location}: {weather_data}")
        # Write the JSON data to a file in the data folder
        try:
            with open(file_path, "a") as f:  # append mode
                json.dump(weather_data, f, indent=4) 
                f.write("\n")  # newline to separate records
        except Exception as e:
            logger.error(f"Error writing JSON for {location}: {e}")
    else:
        logger.warning(f"No current weather data found for {location}")


def parse_location(location: str) -> tuple:
    """Parse location into city, state, and country."""
    parts = location.split(",")
    city = parts[0].strip()
    state = parts[1].strip() if len(parts) > 1 else ""
    country = parts[2].strip() if len(parts) > 2 else ""
    return city, state, country


def main() -> None:
    api_key: str = get_api_key()
    if not api_key:
        logger.error("API key not found. Exiting.")
        return

    logger.info("API Key found")
    locations = read_properties_list()

    if not locations:
        logger.error("No locations found in properties. Exiting.")
        return

    # Run the script for 24 hours
    end_time = datetime.datetime.now() + datetime.timedelta(hours=24)
    while datetime.datetime.now() < end_time:
        for location in locations:
            logger.info(f"Processing location: {location}")
            process_location_for_current_weather(api_key, location)

        logger.info("Waiting for 20 minutes before next update.")
        time.sleep(1200)  # Wait for 20 minutes (1200 seconds)

    logger.info("24-hour data collection complete.")


if __name__ == "__main__":
    main()
