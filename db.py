from pymongo import MongoClient
from os import environ

uri = environ.get('MONGODB_URI', 'mongodb://localhost:27017/gjhm')
client = MongoClient(uri)
db = client.get_default_database()

users = db.users
media = db.media
reviews = db.reviews
playlists = db.playlists
