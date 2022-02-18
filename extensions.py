from flask import session, redirect, url_for
from functools import wraps
import tmdbsimple as tmdb
from db import playlists, users

def current_user():
    return session.get('current_user')

def find_user(username=None, user_id=None):
    """ movie_id is from tmdb's API """
    if username:
        return users.find_one({'username': username})

    return users.find_one({'_id': user_id})

def find_movie(movie_id):
    """ movie_id is from tmdb's API """
    return tmdb.Movies(movie_id).info()

def user_playlists(user_id):
    """ Returns all playlists to belonging user """
    return playlists.find({'user_id': user_id})

def is_authenticated():
    """ Validates if current user is authenticated """
    return True if session.get('current_user') else False

def is_publisher(username):
    """ Checks if current_user is the passed in username """
    return session['current_user']['username'] == username

def login_required(function):
    @wraps(function)
    def wrap(*func, **params):
        if session.get('current_user'):
            return function(*func, **params)
        return redirect(url_for('homepage'))
    return wrap

def logged_out_required(function):
    @wraps(function)
    def wrap(*func, **params):
        if not session.get('current_user'):
            return function(*func, **params)
        return redirect(url_for('homepage'))
    return wrap
