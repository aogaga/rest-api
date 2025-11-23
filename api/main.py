from fastapi import FastAPI
from common import List, Optional, logger
from services.restaurant_service import RestaurantService
from models.restaurant import Restaurant
from cors import add_cors_middleware
restaurantService = RestaurantService()


app = FastAPI()

# Apply CORS middleware
add_cors_middleware(app)

@app.get("/")
def read_root():
    return {"Welcome to the restuarant API"}


@app.get("/search", response_model=List[Restaurant])
async def search(term: Optional[str] = "restaurants", limit: int = 10):
    try:
        result = await restaurantService.search(term, limit)
        if result:
            return result;
    except Exception as ex:
        logger.info("Yelp API error:", ex)