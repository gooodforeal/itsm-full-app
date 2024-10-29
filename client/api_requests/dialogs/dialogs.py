import json
import requests


URL = "http://127.0.0.1:8000"

headers = {
    'Content-Type': 'application/json'
}


def get_messages(token: str, recipient_username: str) -> dict:
    url = URL + "/" + "dialogs/" + "dialog"

    response = requests.post(
        url=url,
        headers=headers,
        data=json.dumps(
            {
                "sender_token": token,
                "recipient_username": recipient_username
            }
        )
    )

    return response.json()


def post_send_message(token: str, recipient_username: str, message: str) -> dict:
    url = URL + "/" + "dialogs/" + "send_message"

    response = requests.post(
        url=url,
        headers=headers,
        data=json.dumps(
            {
                "sender_token": token,
                "recipient_username": recipient_username,
                "message": message
            }
        )
    )

    return response.json()
