import requests
import json


body = {
  "email": "user@example.com",
  "password": "string"
}

headers = {
    'Content-Type': 'application/json'
}

response = requests.post(
    url="http://127.0.0.1:8000/auth/login",
    data=json.dumps(body),
    headers=headers
)
print(response.json())


response = requests.post(url="http://127.0.0.1:8000/auth/logout/")
print(response.json())
