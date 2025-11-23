import os
import logging
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv


#env file
load_dotenv()
#configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)