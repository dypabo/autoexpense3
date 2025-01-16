import requests
from pytest import fixture

from autoexpense3.web_app.constants import APP_URL


@fixture
def homepage_content():
    return requests.get(APP_URL).text
