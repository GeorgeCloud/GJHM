from dotenv import load_dotenv
import os

load_dotenv()

class Config(object):
    """Set environment variables."""

    TMDB_API_KEY= os.getenv('TMDB_API_KEY')
    # SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY')