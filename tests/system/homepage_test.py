from autoexpense3.web_app.constants import APP_NAME, APP_URL
from tests.system.utilities import get_webpage_title


def test_homepage_url_is_https():
    assert APP_URL.startswith("https")


def test_homepage_have_appname_in_title(homepage_content):
    assert APP_NAME in get_webpage_title(homepage_content)
