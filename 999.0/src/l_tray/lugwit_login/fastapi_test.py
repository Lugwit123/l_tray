import requests

data = {
    "username": "newuser",
    "password": "newpassword",
    "email": "user@example.com"
}

response = requests.post("http://127.0.0.1:8000/register/", json=data)
print(response.json())