import requests


def authenticate_user(username, password):
    api_url = "http://localhost:5000/api/users/login"
    credentials = {"username": username, "password": password}
    
    response = requests.post(api_url, json=credentials)
    
    if response.status_code == 200:
        return True
    return False

def register_user(username, email, password, height, weight, birthday):
    api_url = "http://localhost:5000/api/users/add"
    user_data = {
        "username": username,
        "email": email,
        "password": password,
        "height": height,
        "weight": weight,
        "birthday": birthday
    }
    
    response = requests.post(api_url, json=user_data)
    
    if response.status_code == 201:
        return True, None
    return False, response.json().get("errors")
