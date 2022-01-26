from flask import Flask, render_template
from pymongo import MongoClient
from users.users import users_bp
from os import environ

app = Flask(__name__)

uri = environ.get('MONGODB_URI', 'mongodb://localhost:27017/gjhm')
client = MongoClient(uri)
db = client.get_default_database()

users = db.users
media = db.media
reviews = db.reviews
playlists = db.playlists

app.register_blueprint(users_bp, url_prefix='/users')

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(port=8001, debug=True)
