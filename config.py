"""Initialize Config class to access environment variables."""
from dotenv import load_dotenv
import os

load_dotenv()

class Config(object):
    """Set environment variables."""
    TMDB_API_KEY = os.getenv('TMDB_API_KEY')
    SECRET_KEY = os.getenv('SECRET_KEY')
