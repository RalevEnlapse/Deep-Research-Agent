import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    LOCAL_SEARCH_PATH = os.getenv("LOCAL_SEARCH_PATH", "./data")

    @staticmethod
    def get_velocity_api_key():
        return os.getenv("VELOCITY_API_KEY", "")
