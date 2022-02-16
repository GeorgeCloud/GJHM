from flask import render_template, request, session
from extensions import is_authenticated
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
    return render_template('index.html')


if __name__ == '__main__':
    app.run(port=8001, debug=True)
