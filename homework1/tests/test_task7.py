import pytest
import requests

from src import task7


class FakeResponse:
    def raise_for_status(self):
        pass

    def json(self):
        return {"login": "octocat"}


def fake_get(url, timeout):
    assert url == "https://api.github.com/users/octocat"
    assert timeout == 10

    return FakeResponse()


def test_get_github_user(monkeypatch):
    monkeypatch.setattr(task7.requests, "get", fake_get)

    assert task7.get_github_user("octocat") == "octocat"


class ErrorResponse:
    def raise_for_status(self):
        raise requests.HTTPError("GitHub request failed")


def failing_get(url, timeout):
    return ErrorResponse()


def test_get_github_user_error(monkeypatch):
    monkeypatch.setattr(task7.requests, "get", failing_get)

    with pytest.raises(requests.HTTPError):
        task7.get_github_user("octocat")