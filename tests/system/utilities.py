from bs4 import BeautifulSoup
from bs4.element import Tag


def get_first_tag(html: str, tag: str) -> Tag:
    soup = BeautifulSoup(html, features="html.parser")
    tags = soup.select(tag)
    return tags[0]


def get_webpage_title(html: str) -> str:
    return get_first_tag(html, "title").text
