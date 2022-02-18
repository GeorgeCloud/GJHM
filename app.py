from flask import render_template, request, session
from extensions import is_authenticated, current_user
from blueprints.users import users_bp
from blueprints.media import media_bp
from blueprints.auth import auth_bp
import tmdbsimple as tmdb
from db import *

app.register_blueprint(users_bp, url_prefix='/users')
app.register_blueprint(media_bp, url_prefix='/media')
app.register_blueprint(auth_bp, url_prefix='/')

api_search = tmdb.Search()

@app.route('/', methods=['GET'])
def homepage():
    trending_media = tmdb.Trending().info()['results']
    popular_movies = tmdb.Discover().movie()['results']
    popular_tvshows = tmdb.Discover().tv()['results']

    return render_template('index.html',
        trending_media=trending_media, popular_movies=popular_movies,
        popular_tvshows=popular_tvshows, current_user=current_user())


if __name__ == '__main__':
    app.run(port=8001, debug=True)
