from pydantic import BaseModel
from typing import Optional, List

class Restaurant(BaseModel):
    id: str
    name: str
    address: Optional[str]
    city: Optional[str]
    rating: Optional[float]
    phone: Optional[str]
    url: Optional[str]
    categories: Optional[List[str]]
    distance_meters: Optional[float]
