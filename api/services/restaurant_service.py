
from core.common import logger, List, Optional, Dict, Any
from services.yelp_api_service import YelpApiService
from models.restaurant import Restaurant
from core.config import LOCATION
from services.redis_service import RedisService

class RestaurantService:
    def __init__(self, redis_service: RedisService = None, yelp: YelpApiService = None):
        self.redis_service = redis_service or RedisService()
        self.yelp = yelp or YelpApiService()
    async def search(self, term: Optional[str] = "restaurants", limit: int = 20) -> List[Restaurant]:
        cache_key = f"yelp:{LOCATION}:{term}:{limit}"
        cached_data = await self.redis_service.get(cache_key)
        restaurants: List[Restaurant] = []

        if cached_data:
            logger.info("Data exists in cache: reading data from cache")
            try:
                for r in cached_data:  # assuming redis_service.get returns a list of dicts
                    try:
                        restaurants.append(Restaurant(**r))
                    except TypeError as e:
                        logger.warning("Failed to reconstruct Restaurant from cache: %s", e)
            except Exception as e:
                logger.warning("Error processing cached data: %s", e)
            return restaurants

        try:
            logger.info("Searching Yelp for term: %s, location: %s, limit: %d", term, LOCATION, limit)
            results = await self.yelp.search(term, LOCATION, limit)

            if results:
                logger.info("Found %d businesses", len(results))
                restaurants = [self._business_to_restaurant(biz) for biz in results]

            # Cache the result (even if empty) using model_dump()
            await self.redis_service.set(cache_key, [r.model_dump() for r in restaurants], ex=600)

            if not restaurants:
                logger.info("No businesses found for term='%s'", term)

            return restaurants

        except Exception:
            logger.exception("Yelp API error occurred")
            return []

    @staticmethod
    def _business_to_restaurant(biz: Dict[str, Any]) -> Restaurant:
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
