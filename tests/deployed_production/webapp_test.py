from autoexpense3.web_app.constants import APP_NAME
from autoexpense3.web_app.constants import APP_URL
from tests.deployed_stagging.utilities import get_webpage_expenses
from tests.deployed_stagging.utilities import get_webpage_title


def test_homepage_url_is_https() -> None:
    """Make sure we are using a SSL connection for the tests."""
    assert APP_URL.startswith("https")


def test_homepage_have_appname_in_title(homepage_content: str) -> None:
    assert APP_NAME in get_webpage_title(homepage_content)


def test_expenses_are_listed(homepage_content: str) -> None:
    """Test the app is setup properly.

    If no expense are listed on the homepage, the repository is probably not working.
    """
    assert len(get_webpage_expenses(homepage_content)) > 0
