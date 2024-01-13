# util_properties.py

import configparser
import pathlib
from utils.util_log import logger


def read_property() -> str:
    """Read a single location from the properties file"""
    config = configparser.ConfigParser()
    config.read(get_properties_file())

    # Loop through the keys in the "DEFAULT" section
    for key in config["DEFAULT"]:
        if key.startswith("location"):
            # Return the first location found
            return config["DEFAULT"][key]

    # Return None or a default value if no location is found
    return None


def read_properties_list() -> list:
    """Read location from the properties file"""
    config = configparser.ConfigParser()
    config.read(get_properties_file())
    locations: list = []
    for key in config["locations"]:
        if key.startswith("location"):
            locations.append(config["locations"][key])
    return locations


def get_properties_file() -> str:
    """
    Return the path to the properties file in my parent directory.
    """
    s = pathlib.Path.cwd().joinpath("config").joinpath("location.properties")
    logger.info(f"Reading from {s}.")
    return s


def main() -> None:
    location = read_property()
    locations = read_properties_list()
    print(location)
    print(locations)


if __name__ == "__main__":
    main()
