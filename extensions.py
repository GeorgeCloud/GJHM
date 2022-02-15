from flask import session, redirect, url_for
from functools import wraps
import tmdbsimple as tmdb

def find_movie(movie_id):
    return tmdb.Movies(movie_id).info()

def is_authenticated():
    return True if session.get('current_user') else False

def login_required(function):
    @wraps(function)
    def wrap(*func, **params):
        if session.get('current_user'):
            return function(*func, **params)
        return redirect(url_for('homepage'))
    return wrap
