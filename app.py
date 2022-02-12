from flask import Flask, render_template, request
import tmdbsimple as tmdb
from db import *

app = Flask(__name__)
api_search = tmdb.Search()

from blueprints.users import users_bp
from blueprints.media import media_bp
from blueprints.auth import auth_bp

app.register_blueprint(users_bp, url_prefix='/users')
app.register_blueprint(media_bp, url_prefix='/media')
app.register_blueprint(auth_bp, url_prefix='/')


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'GET':
        return render_template('search.html')

    search_query = request.form["search_query"]
    movies = api_search.movie(query=search_query)['results'][:3]

    return render_template('search.html', search_query=search_query, movies=movies)


if __name__ == '__main__':
    app.run(port=8001, debug=True)
