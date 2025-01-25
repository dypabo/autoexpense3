from bs4 import BeautifulSoup
from bs4.element import Tag


def _get_first_tag(html: str, tag: str) -> Tag:
    """In an HTML string, return the the first matching tag."""
    soup = BeautifulSoup(html, features="html.parser")
    tags = soup.select(tag)
    return tags[0]


def get_webpage_title(html: str) -> str:
    """Return the webpage title string for an HTML string."""
    return _get_first_tag(html, "title").text
