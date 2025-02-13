import requests
from autoexpense3.web_app.constants import APP_NAME
from autoexpense3.web_app.constants import APP_URL
from tests.utilities_html import get_webpage_title


def test_homepage_url_is_https() -> None:
    """Make sure we are using a SSL connection for the tests."""
    assert APP_URL.startswith("https")


def test_homepage_have_appname_in_title(homepage_content: str) -> None:
    print(requests.get("https://google.ca"))
    print(requests.get(APP_URL))
    assert APP_NAME in get_webpage_title(homepage_content)
