from fastapi import APIRouter
from services.restaurant_service import Restaurant
from typing import Optional, List
import os

restaurantService = Restaurant()
router = APIRouter()


@router.get("/search", response_model=List[Restaurant])
async def search(term: Optional[str] = "restaurants", limit: int = 10):
    try:
        result = await restaurantService.search(term, limit)
        if result:
            return result;
    except Exception as ex:
        print("Yelp API error:", ex)