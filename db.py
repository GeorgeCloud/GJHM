from flask import Flask
from flask_pymongo import pymongo
from pymongo import MongoClient
from flask_login import LoginManager, current_user
from flask_bcrypt import Bcrypt
from os import environ

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = '##-##<F>Society##-##'

# ======= DB Setup ==========
CONNECTION_STRING = 'mongodb+srv://GJHM:Gjhm111!@cluster0.bfwfn.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'
client = pymongo.MongoClient(CONNECTION_STRING)
# uri = environ.get('MONGODB_URI', 'mongodb://localhost:27017/gjhm')
# client = MongoClient(uri)
db = client.get_default_database()
# ===========================


# ======= Collections ==========
users = db.users
media = db.media
reviews = db.reviews
playlists = db.playlists
# =========================


# ======= Authentication ==========
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.view'

@login_manager.user_loader
def load_user(user_id):
    return users.find_one({'_id': user_id})
# =================================
