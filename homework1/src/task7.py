"""Task 7: Using the requests package."""

import requests


def get_github_user(username):
    """Return a GitHub username from the GitHub API."""
    url = f"https://api.github.com/users/{username}"

    response = requests.get(url, timeout=10)
    response.raise_for_status()

    return response.json()["login"]


def main():
    """Show an example request using the requests package."""
    print(get_github_user("octocat"))


if __name__ == "__main__":
    main()