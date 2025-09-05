"""Functions that interact with the Postcode API."""

import os.path
import json

import requests as req


CACHE_FILE = "./postcode_cache.json"
TEST_FILE = "./test_cache.json"


def load_cache() -> dict:
    """Loads the cache from a file and converts it from JSON to a dictionary."""
    cached_data = {}

    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r", encoding="utf-8") as file:
            cached_data = json.load(file)

    return cached_data


def save_cache(cache: dict) -> None:
    """Saves the cache to a file as JSON"""
    with open(CACHE_FILE, "w", encoding="utf-8") as file:
        json.dump(cache, file)


def validate_postcode(postcode: str) -> bool:
    """Use API to validate postcode"""

    if not isinstance(postcode, str):
        raise TypeError("Function expects a string.")

    url = f"https://api.postcodes.io/postcodes/{postcode}/validate"

    cached_data = load_cache()

    if postcode in cached_data:
        is_valid = cached_data[postcode].get("valid")
        return is_valid

    response = req.get(url, timeout=10)

    if response.status_code == 500:
        raise req.RequestException("Unable to access API.")

    response_json = response.json()
    is_valid = response_json.get("result")

    cached_data.update({postcode: {"valid": is_valid}})
    save_cache(cached_data)

    return is_valid


def get_postcode_for_location(lat: float, long: float) -> str:
    """Use API to get nearest postcode for a given longitude and latitude"""

    if not isinstance(lat, float) or not isinstance(long, float):
        raise TypeError("Function expects two floats.")

    url = f"https://api.postcodes.io/postcodes?lon={long}&lat={lat}"

    response = req.get(url, timeout=10)

    if response.status_code == 500:
        raise req.RequestException("Unable to access API.")

    response_json = response.json()
    result = response_json.get("result")

    if result is None:
        raise ValueError("No relevant postcode found.")

    postcodes = []

    for _ in result:
        postcode = _.get("postcode")
        postcodes.append(postcode)

    return postcodes[0]


def get_postcode_completions(postcode_start: str) -> list[str]:
    """Use API to autocomplete postcodes"""

    if not isinstance(postcode_start, str):
        raise TypeError("Function expects a string.")

    url = f"https://api.postcodes.io/postcodes/{postcode_start}/autocomplete"

    cached_data = load_cache()
    if postcode_start in cached_data:
        completions = cached_data[postcode_start].get("completions")
        return completions

    response = req.get(url, timeout=10)

    if response.status_code == 500:
        raise req.RequestException("Unable to access API.")

    response_json = response.json()
    result = response_json.get("result")

    if result is None:
        raise ValueError("No relevant postcode found.")

    # SAVE TO CACHE WHEN DONE IF IT EXISTS
    cached_data.update({postcode_start: {"completions": result}})
    save_cache(cached_data)

    return result


def get_postcodes_details(postcodes: list[str]) -> dict:
    """Use API to get details of multiple postcodes"""

    if not isinstance(postcodes, list):
        raise TypeError("Function expects a list of strings.")

    for postcode in postcodes:
        if not isinstance(postcode, str):
            raise TypeError("Function expects a list of strings.")

    url = "https://api.postcodes.io/postcodes"
    data = {"postcodes": postcodes}

    response = req.post(url, data, timeout=10)

    if response.status_code == 500:
        raise req.RequestException("Unable to access API.")

    response_json = response.json()

    return response_json
