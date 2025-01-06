import os
import requests
from dotenv import load_dotenv
import json


load_dotenv()

RAPID_API_KEY = os.getenv("RAPID_API_KEY")


def remove_empty_pairs(json_obj):
    if isinstance(json_obj, dict):
        return {
            key: remove_empty_pairs(value)
            for key, value in json_obj.items()
            if value is not None and remove_empty_pairs(value)
        }
    elif isinstance(json_obj, list):
        return [
            remove_empty_pairs(item)
            for item in json_obj
            if item is not None and remove_empty_pairs(item)
        ]
    else:
        return json_obj


def scrape_linkedin_data(name):

    url = "https://linkedin-data-api.p.rapidapi.com/data-connection-count"

    querystring = {"username": name}

    headers = {
        "x-rapidapi-key": f"{RAPID_API_KEY}",
        "x-rapidapi-host": "linkedin-data-api.p.rapidapi.com",
    }

    response = requests.get(url, headers=headers, params=querystring)

    return response.json()


def get_linkedin_data(name):
    response = scrape_linkedin_data(name)
    cleaned_response = remove_empty_pairs(response)
    return cleaned_response


if __name__ == "__main__":

    response = get_linkedin_data(name="juliacervantesespinoza")
    print(response)
