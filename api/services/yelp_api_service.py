from typing import List, Dict, Any, Optional
import httpx
from common import logger, List
from config import YELP_BASE

class YelpApiService:
    def __init__(self, api_key: Optional[str]):
        self.api_key = api_key
        self.headers = (
            {"Authorization": f"Bearer {self.api_key}"} if self.api_key else {}
        )
    async def search(self, term: str, location: str, limit: int = 10) -> List[Dict[str, Any]]:
        if not self.api_key:
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

        # Return empty list if an exception occurred
        return []
