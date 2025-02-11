from playwright.sync_api import Page
from playwright.sync_api import expect

from autoexpense3.web_app.constants import APP_NAME


def test_app_name_in_homepage_title(homepage: Page) -> None:
    expect(homepage).to_have_title(APP_NAME)
