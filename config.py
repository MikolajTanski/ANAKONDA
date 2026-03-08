class Config:
    MONGO_URI = "mongodb://127.0.0.1:27017"
    DB_NAME = "Scrapper"
    COLLECTION_NAME = "otodom_listings"

    BASE_URL = "https://www.otodom.pl/pl/wyniki/sprzedaz/mieszkanie/cala-polska"
    MAX_PAGES = 25      # None = do końca
    DELAY_MIN = 3.0
    DELAY_MAX = 7.0

    HEADERS = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/122.0.0.0 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://www.otodom.pl/",
        "DNT": "1",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
    }
