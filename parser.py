import logging
from datetime import datetime

log = logging.getLogger(__name__)


class OtodomParser:
    """Parsuje __NEXT_DATA__ i zwraca ustrukturyzowane ogłoszenia."""

    def get_total_pages(self, next_data: dict) -> int:
        try:
            pagination = next_data["props"]["pageProps"]["data"]["searchAds"]["pagination"]
            return pagination.get("totalPages", 1)
        except (KeyError, TypeError):
            return 1

    def extract_listings(self, next_data: dict) -> list[dict]:
        try:
            items = next_data["props"]["pageProps"]["data"]["searchAds"]["items"]
        except (KeyError, TypeError):
            log.warning("Nie znaleziono items w __NEXT_DATA__")
            return []

        listings = []
        for item in items:
            listing = {
                "id": item.get("id"),
                "slug": item.get("slug"),
                "title": item.get("title"),
                "url": "https://www.otodom.pl/pl/oferta/" + item.get("slug", ""),
                "price": self._get(item, "totalPrice", "value"),
                "price_currency": self._get(item, "totalPrice", "currency"),
                "price_per_m2": self._get(item, "pricePerSquareMeter", "value"),
                "area": self._get(item, "areaInSquareMeters"),
                "rooms": self._get(item, "roomsNumber"),
                "floor": self._get(item, "floor"),
                "location_city": self._get(item, "location", "address", "city", "name"),
                "location_district": self._get(item, "location", "address", "district", "name"),
                "location_street": self._get(item, "location", "address", "street", "name"),
                "lat": self._get(item, "location", "mapDetails", "lat"),
                "lng": self._get(item, "location", "mapDetails", "lon"),
                "agency": self._get(item, "agency", "name"),
                "is_private": item.get("isPrivateOwner"),
                "date_created": item.get("dateCreatedFirst"),
                "images_count": len(item.get("images") or []),
                "scraped_at": datetime.utcnow(),
            }
            if listing["id"]:
                listings.append(listing)

        return listings

    @staticmethod
    def _get(obj, *keys):
        for key in keys:
            if not isinstance(obj, dict):
                return None
            obj = obj.get(key)
        return obj
