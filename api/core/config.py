# config.py
from core.common import os, logger

YELP_API_KEY = os.getenv("YELP_API_KEY")
LOCATION = os.getenv("LOCATION")
YELP_BASE = os.getenv("YELP_BASE")
REDIS_URL = os.getenv("REDIS_URL")

if not YELP_API_KEY:
    logger.error("YELP_API_KEY environment variable not set")
    raise ValueError("YELP_API_KEY environment variable not set")
