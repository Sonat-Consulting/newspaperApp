import pytest
from extractor import extract_articles


@pytest.mark.parametrize("url, amount, expected_amount", [
    ("http://vg.no", 1, 1),
    ("https://vg.no", 20, 20),
    ("vg.no", 6, 6),
    ("nrk.no", 12, 12),
    ("https://nrk.no", 13, 13),
    ("http://nrk.no", 16, 16),
    ("ba.no", 7, 7),
    ("http://cnn.com", 16, 16),
    ("https://cnn.com", 11, 11),
    ("http://dagbladet.no", 0, 0)

])
def test_extract_articles_amount_valid_input(url, amount, expected_amount):
    data = extract_articles(url, amount)
    assert type(data) == dict
    assert "content" in data
    assert "failed" in data
    assert "total" in data
    assert len(data["content"]) == expected_amount


@pytest.mark.parametrize("url, amount, expected_amount", [
    ("://nrk.no", 16, 0),
    ("", 16, 0),
    ("http://vg.no", 1, 1),
    ("         ", 100, 0)
])
def test_extract_arcles_amount_invalid_input(url, amount, expected_amount):
    data = extract_articles(url, amount)
    assert type(data) == dict
    assert "content" in data
    assert "failed" in data
    assert "total" in data
    assert len(data["content"]) == expected_amount


def test_extract_articles_check_for_errors():
    with pytest.raises(AttributeError):
        extract_articles(None, 100)

    with pytest.raises(AttributeError):
        extract_articles(None, None)


