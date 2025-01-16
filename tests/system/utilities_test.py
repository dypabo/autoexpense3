from tests.system.utilities import get_webpage_title


def test_get_title_extract():
    assert "TITLE" == get_webpage_title(
        """<html><title>TITLE</title><body>BODY</body></html>"""
    )
