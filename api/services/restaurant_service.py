from typing import List, Optional
from models.restaurant import Restaurant
from services.yelp_api_service import YelpApiService
import os

YELP_API_KEY = os.getenv("YELP_API_KEY")
LOCATION = os.getenv("LOCATION")
if not YELP_API_KEY:
    raise ValueError("YELP_API_KEY environment variable not set")

yelp = YelpApiService(YELP_API_KEY)

class RestaurantService:

    async def search(self, term: Optional[str] = "restaurants",  limit: int = 10) -> List[Restaurant]:
        try:
            results = await yelp.search(term, LOCATION, limit)
            if results:
                return [self._business_to_rest(b) for b in results]
            return []
        except Exception as ex:
            print("Yelp API error:", ex)
            return []


    @staticmethod
    def business_to_rest(self, biz) -> Restaurant:
        return Restaurant(
            id=biz.get("id"),
            name=biz.get("name"),
            address=", ".join(biz.get("location", {}).get("display_address", [])),
            city=biz.get("location", {}).get("city"),
            rating=biz.get("rating"),
            phone=biz.get("display_phone"),
            url=biz.get("url"),
            categories=[c.get("title") for c in biz.get("categories", [])],
            distance_meters=biz.get("distance")
        )
