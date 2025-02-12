from tests.utilities_html import get_webpage_title


def test_get_title_extract() -> None:
    assert (
        get_webpage_title(
            """<html><title>TITLE</title><body>BODY</body></html>""",
        )
        == "TITLE"
    )
