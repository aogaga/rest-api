from typing import  Dict, Any, Optional
import httpx
from common import logger, List
from config import YELP_BASE, YELP_API_KEY

class YelpApiService:
    def __init__(self):

        self.headers = self.headers = {"Authorization": f"Bearer {YELP_API_KEY}"}

    async def search(self, term: str, location: str, limit: int = 10) -> List[Dict[str, Any]]:
        if not YELP_API_KEY:
            logger.warning("Yelp API key is not configured.")
            return []

        params = {
            "term": term or "restaurant",
            "location": location,
            "limit": limit,
        }

        try:
            async with httpx.AsyncClient(timeout=10) as client:
                response = await client.get(
                    f"{YELP_BASE}/businesses/search",
                    headers=self.headers,
                    params=params
                )
                response.raise_for_status()
                return response.json().get("businesses", [])

        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
        except httpx.RequestError as e:
            logger.error(f"Request error occurred: {e}")
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")
        return []
