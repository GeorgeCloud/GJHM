from flask import Flask
from pymongo import MongoClient
from flask_login import LoginManager, current_user
from flask_bcrypt import Bcrypt
from os import environ
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
bcrypt = Bcrypt(app)
app.secret_key = '##-##<F>Society##-##'

# ======= DB Setup ==========
uri = environ.get('MONGODB_URI', 'mongodb://localhost:27017/gjhm')
client = MongoClient(uri)
db = client.get_default_database()
# ===========================


# ======= Collections ==========
users = db.users
users.create_index('username', unique=True)
playlists = db.playlists
media = db.media
reviews = db.reviews
# =========================


# ======= Authentication ==========
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.view'

@login_manager.user_loader
def load_user(user_id):
    return users.find_one({'_id': user_id})
# =================================
