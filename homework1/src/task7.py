import requests


def get_github_user(username):
    url = f"https://api.github.com/users/{username}"

    response = requests.get(url, timeout=10)

    response.raise_for_status()

    return response.json()["login"]