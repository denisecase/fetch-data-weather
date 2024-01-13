# util_location.py

import configparser
import csv
import pathlib
import requests
from utils.util_api import get_api_key
from utils.util_log import logger

COORDS_DICT = {}

def get_location_coords_csv_file() -> str:
    """
    Return the path to the location_coords.csv file in my parent directory.
    """
    s: str = pathlib.Path.cwd().joinpath("data").joinpath("location_coords.csv")
    logger.info(f"Reading from {s}.")
    return s


def get_coords_from_csv(location):
    """Get coordinates from CSV if available."""
    return COORDS_DICT.get(location)


def load_coords_from_csv():
    """Load the coordinates from the CSV into a global dictionary."""
    try:
        with open(get_location_coords_csv_file(), mode="r") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                city, state, country, lat, lon = row.values()
                COORDS_DICT[f"{city},{state},{country}"] = (lat, lon)
        logger.info("CSV data loaded successfully.")
    except FileNotFoundError:
        logger.error("CSV file not found.")
    except Exception as e:
        logger.error(f"Error loading CSV: {e}")


def get_lat_lon(location, api_key):
    """Get from location_coords.csv if available, otherwise fetch from API."""
    if not COORDS_DICT:
        load_coords_from_csv()
    for loc in COORDS_DICT:
        logger.info(f"Checking {loc} against {location}")
        if loc == location:
                lat, lon = COORDS_DICT[loc]
                logger.info(f"Coordinates for {loc} found in csv: {lat},{lon}")
                return (lat, lon)
    # Fallback to API if not found - test with fake coords to avoid hitting API limit
    return (1,2 )
    # return fetch_lat_lon(location, api_key)


def fetch_lat_lon(location, api_key) -> tuple:
    """
    Fetches latitude and longitude for a given location using OpenWeatherMap Geocoding API.

    :param location: A string in the format 'City, State Code, Country Code' (e.g., 'Ely, MN, US')
    :param api_key: Your OpenWeatherMap API key
    :return: A tuple (latitude, longitude) or (None, None) if not found
    """
    # Parse the location
    city, state, country = parse_location(location)

    # Construct the API URL
    url = f"http://api.openweathermap.org/geo/1.0/direct?q={city},{state},{country}&limit=1&appid={api_key}"
    logger.info(f"Fetching url: {url}")
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data:
                # Assuming the first result is the most relevant
                return data[0]["lat"], data[0]["lon"]
            else:
                return None, None
        else:
            print(f"Error fetching data: HTTP {response.status_code}")
            return None, None
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return None, None


def parse_location(location: str) -> tuple:
    """Parse location into city, state, and country."""
    parts = location.split(",")
    city = parts[0].strip()
    state = parts[1].strip() if len(parts) > 1 else ""
    country = parts[2].strip() if len(parts) > 2 else ""
    return city, state, country


def main():
    api_key: str = get_api_key()
    load_coords_from_csv()
    locations = [
        "Austin,TX,US",
        "Cupertino,CA,US",
        "Dublin,,IE",
        "Ely,NV,US",
        "Folsom,CA,US",
        "Kansas City,MO,US",
        "Maryville,MO,US",
        "Minneapolis,MN,US",
        "Olathe,KS,US",
        "Seattle,WA,US",
        "Spokane,WA,US",
        "Wichita,KS,US",
    ]

    for location in locations:
        city, state, country = parse_location(location)
        coords = get_coords_from_csv(location)

        if coords:
            logger.info(f"{location} found in CSV: {coords}")
        else:
            lat, lon = fetch_lat_lon(location, api_key)
            if lat is not None and lon is not None:
                logger.info(f"{location}={lat},{lon} (API)")
            else:
                logger.info("Location not found or API error occurred.")


if __name__ == "__main__":
    main()
