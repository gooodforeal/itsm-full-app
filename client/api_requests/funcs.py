import json

import requests



URL = "http://127.0.0.1:8000"

headers = {
    'Content-Type': 'application/json'
}


def get_service(service_id: int) -> dict:
    url = URL + "/" + "services/" + "service/" + str(service_id)

    response = requests.get(
        url=url,
        headers=headers
    )

    return response.json()


def get_statuses() -> dict:
    url = URL + "/" + "incidents/" + "statuses/" + "all"

    response = requests.get(
        url=url,
        headers=headers
    )

    return response.json()


def get_incident(incident_id: int) -> dict:
    url = URL + "/" + "incidents/" + "incident/" + str(incident_id)

    response = requests.get(
        url=url,
        headers=headers
    )

    return response.json()


def get_services() -> dict:
    url = URL + "/" + "services/" + "all"

    response = requests.get(
        url=url,
        headers=headers
    )

    return response.json()


def post_incidents(token: str) -> dict:
    url = URL + "/" + "incidents/" + "all"

    response = requests.post(
        url=url,
        headers=headers,
        data=json.dumps(
            {
                "token": token,
            }
        )
    )

    return response.json()


def post_incidents_admin(token: str) -> dict:
    url = URL + "/" + "incidents/" + "admin/" + "all"

    response = requests.post(
        url=url,
        headers=headers,
        data=json.dumps(
            {
                "token": token,
            }
        )
    )

    return response.json()


def post_create_incident(token: str, line: str, name: str, desc: str) -> dict:
    url = URL + "/" + "incidents/" + "create"

    response = requests.post(
        url=url,
        headers=headers,
        data=json.dumps(
            {
                "token": token,
                "service_line_name": line,
                "incident_name": name,
                "incident_description": desc
            }
        )
    )

    return response.json()


def get_service_lines() -> dict:
    url = URL + "/" + "services/" + "lines/" + "all"

    response = requests.get(
        url=url,
        headers=headers
    )

    return response.json()


def post_is_admin(token: str):
    url = URL + "/" + "auth/" + "is_admin"

    response = requests.post(
        url=url,
        headers=headers,
        data=json.dumps(
            {
                "token": token,
            }
        )
    )
    return response.json()


def post_is_tech(token: str):
    url = URL + "/" + "auth/" + "is_tech"

    response = requests.post(
        url=url,
        headers=headers,
        data=json.dumps(
            {
                "token": token,
            }
        )
    )
    return response.json()


def post_create_service(token: str, type_name: str, line_name: str, name: str, description: str):
    url = URL + "/" + "services/" + "create"

    response = requests.post(
        url=url,
        headers=headers,
        data=json.dumps(
            {
                "token": token,
                "service_type_name": type_name,
                "service_line_name": line_name,
                "service_name": name,
                "service_description": description
            }
        )
    )

    return response.json()


def post_edit_service(token: str, id: int, name: str, description: str):
    url = URL + "/" + "services/" + "edit"

    response = requests.post(
        url=url,
        headers=headers,
        data=json.dumps(
            {
                "token": token,
                "service_id": id,
                "service_name": name,
                "service_description": description
            }
        )
    )

    return response.json()


def post_delete_service(token: str, service_id: int):
    url = URL + "/" + "services/" + "delete"

    response = requests.post(
        url=url,
        headers=headers,
        data=json.dumps(
            {
                "token": token,
                "service_id": service_id,
            }
        )
    )

    return response.json()


def api_login(username, password) -> dict:
    url = URL + "/" + "auth/" + "login"

    response = requests.post(
        url=url,
        headers=headers,
        data=json.dumps(
            {
                "username": username,
                "password": password
            }
        )
    )

    return response.json()


def api_register(fio: str, username: str, password: str) -> dict:
    url = URL + "/" + "auth/" + "register"

    response = requests.post(
        url=url,
        headers=headers,
        data=json.dumps(
            {
                "fio": fio,
                "username": username,
                "password": password
            }
        )
    )

    return response.json()


def post_edit_incident(token: str, incident_id: int, status: str) -> dict:
    url = URL + "/" + "incidents/" + "edit"

    response = requests.post(
        url=url,
        headers=headers,
        data=json.dumps(
            {
                "token": token,
                "incident_id": incident_id,
                "incident_status_name": status
            }
        )
    )

    return response.json()

