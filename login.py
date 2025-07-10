import json
import os
import requests
from cliColors import info, success, warning, error, prompt


def load_llm_credentials(credentials_file):
    if os.path.exists(credentials_file):
        with open(credentials_file, "r") as f:
            return json.load(f)
    return {}

def save_llm_credentials(credentials, credentials_file):
    with open(credentials_file, "w") as f:
        json.dump(credentials, f)


def load_credentials(credentials_file):
    if os.path.exists(credentials_file):
        return json.load(open(credentials_file, 'r'))
    return None

def save_credentials(username, password, credentials_file):
    with open(credentials_file, 'w') as f:
        json.dump({"username": username, "password": password}, f)
    success("Credentials saved for future use.")

def login_and_get_jwt(credentials_file, login_url):
    session = requests.Session()
    creds = load_credentials(credentials_file)

    if creds:
        use_saved = prompt("Use saved credentials? (y/n):").lower() == 'y'
        if use_saved:
            username, password = creds["username"], creds["password"]
        else:
            username = prompt("Enter username:")
            password = prompt("Enter password:")
    else:
        username = prompt("Enter username:")
        password = prompt("Enter password:")

    info("Logging in...")
    login_data = {'login': username, 'password': password}
    response = session.post(login_url, data=login_data)

    if response.status_code != 200 or 'JWT-SESSION' not in session.cookies:
        error("Login failed or JWT token not found.")
        raise Exception("Login failed.")

    jwt_token = session.cookies.get('JWT-SESSION')
    success("Logged in successfully. JWT Token retrieved.")

    if not creds:
        save = prompt("Save credentials for future use? (y/n):").lower() == 'y'
        if save:
            save_credentials(username, password, credentials_file)

    return session, jwt_token

def logout(session, sonar_url):
    info("Logging out...")
    logout_url = f"{sonar_url}/sessions/logout"
    response = session.get(logout_url)
    if response.status_code == 200:
        success("Logged out successfully.")
    else:
        warning(f"Logout failed with status code {response.status_code}.")
    session.close()