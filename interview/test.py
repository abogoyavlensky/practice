import pytest
from revolut import UrlShortener

def test_store_url():
    shortener = UrlShortener()

    original_url = "https://www.test.com/test-path/"
    shortener.store_url(original_url)

    assert len(shortener.storage) == 1
    assert shortener.storage.get("https://www.rev.me/1") == original_url

def test_get_full_url():
    shortener = UrlShortener()

    original_url_1 = "https://www.test.com/test-path-1/"
    shortener.store_url(original_url_1)

    original_url_2 = "https://www.test.com/test-path-2/"
    shortener.store_url(original_url_2)

    short_url_2 = "https://www.rev.me/2"

    assert len(shortener.storage) == 2
    assert shortener.get_full_url(short_url_2) == original_url_2

def test_max_urls_exception():
    shortener = UrlShortener(2)

    original_url_1 = "https://www.test.com/test-path-1/"
    shortener.store_url(original_url_1)

    original_url_2 = "https://www.test.com/test-path-2/"
    shortener.store_url(original_url_2)

    with pytest.raises(Exception):
        original_url_3 = "https://www.test.com/test-path-3/"
        shortener.store_url(original_url_3)

    assert len(shortener.storage) == 2
    assert shortener.storage.get(original_url_3) == None
