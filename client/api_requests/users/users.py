import json
import requests


URL = "http://127.0.0.1:8000"

headers = {
    'Content-Type': 'application/json'
}


def get_users() -> dict:
    url = URL + "/" + "auth/" + "all"

    response = requests.get(
        url=url,
        headers=headers
    )

    return response.json()
