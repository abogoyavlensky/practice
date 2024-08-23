# Task
# For a given URL, generate a short URL and retrieve the original by the generated one. 

# Input:
# https://www.revolut.com/rewards-personalised-cashback-and-discounts/

# Expected output:
# https://www.rev.me/<url identifier>

STORAGE = {}
BASE_URL = "https://www.rev.me/"


class UrlShortener():
    def __init__(self, max_urls_count = 100) -> None:
        self.storage = {}
        self.max_urls_count = max_urls_count

    def get_short_url_idx(self):
        last_idx = len(self.storage)
        return last_idx + 1

    def generate_short_url(self):
        url_idx = self.get_short_url_idx()
        return f"{BASE_URL}{url_idx}"

    def store_url(self, full_url):
        result_url = self.generate_short_url()
        if len(self.storage) + 1 > self.max_urls_count:
            raise Exception("Maximum urls reached")
        else:
            self.storage[result_url] = full_url

    def get_full_url(self, short_url):
        return self.storage.get(short_url)
