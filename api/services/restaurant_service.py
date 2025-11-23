
from common import  logger, List, Optional
from services.yelp_api_service import YelpApiService
from models.restaurant import Restaurant
from config import YELP_API_KEY, LOCATION

# Yelp API client
yelp = YelpApiService(YELP_API_KEY)

class RestaurantService:

    async def search(self, term: Optional[str] = "restaurants",  limit: int = 10) -> List[Restaurant]:
        try:
            logger.info("api key is %s", YELP_API_KEY)
            logger.info("Searching Yelp for term: %s, location: %s, limit: %d", term, LOCATION, limit)

            results = await yelp.search(term, LOCATION, limit)
            if results:
                logger.info("Found %d businesses", len(results))
                restaurants = []
                for biz in results:
                    restaurants.append(Restaurant(
                        id=biz.get("id"),
                        name=biz.get("name"),
                        address=", ".join(biz.get("location", {}).get("display_address", [])),
                        city=biz.get("location", {}).get("city"),
                        rating=biz.get("rating"),
                        phone=biz.get("display_phone"),
                        url=biz.get("url"),
                        categories=[c.get("title") for c in biz.get("categories", [])],
                        distance_meters=biz.get("distance")
                    ))
                return restaurants
            logger.info("No businesses found for term='%s'", term)
            return []
        except Exception as ex:
            logger.exception("Yelp API error occurred", ex)
            return []