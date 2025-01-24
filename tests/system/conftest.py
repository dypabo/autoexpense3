import pytest
import requests

from autoexpense3.web_app.constants import APP_URL


@pytest.fixture
def homepage_content() -> str:
    """Return the html string of homepage."""
    return requests.get(APP_URL, timeout=3).text
