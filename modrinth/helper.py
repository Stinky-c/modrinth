from .models import *
from .exceptions import *
import requests as req


@staticmethod
def _get(url: str, headers: dict, **kwargs) -> req.Response:
    """Returns Json from url, raises BadRequest if not 200"""

    res = req.get(url, headers=headers)

    if res.status_code == 200:
        return res.json()
    else:
        raise BadRequest(f"'{url}' Returned a {res.status_code}")


@staticmethod
def _get_u(url: str, headers: dict, **kwargs) -> req.Response:
    """Returns url too"""
    return _get(url, headers, **kwargs), url


@staticmethod
def _download(url: str, headers: dict):
    res = req.get(url, headers=headers)
    if res.status_code == 200:
        return res.content
    else:
        raise BadRequest(f"'{url}' Returned a {res.status_code}")
