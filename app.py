from flask import Flask, render_template, request
from blueprints.users import users_bp
from blueprints.media import media_bp
from db import *

app = Flask(__name__)

app.register_blueprint(users_bp, url_prefix='/users')
app.register_blueprint(media_bp, url_prefix='/media')

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    search_query = request.form["search_query"]
    # found_users = users.find({})
    # found_media = 
    # found_playlists = 
    return render_template('search.html', search_query=search_query)

if __name__ == '__main__':
    app.run(port=8001, debug=True)
