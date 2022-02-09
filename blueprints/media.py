from flask import Blueprint, render_template, request, redirect, url_for
from datetime import datetime
from bson.objectid import ObjectId
import tmdbsimple as tmdb
from db import *

media_bp = Blueprint('media_bp', __name__, template_folder='templates')
api_search = tmdb.Search()

@media_bp.route('/', methods=['GET'])
def index_media():
    """Return ALL media"""
    return render_template('media_index.html', media=media.find())


@media_bp.route('/create', methods=['POST'])
def create_movie(user_id):
    """Creates new media to db"""
    user = users.find_one({'_id': ObjectId(user_id)})
    media_type = request.form['type']
    media_item = {
        'type':            media_type,
        'title':           request.form['title'],
        'genre':           request.form['genre'],           # gets removed for ytvid type
        'year_created':    request.form['year_created'],
        'date_watched':    request.form['date_watched'],
        'acts_dirs':       request.form['act_dirs'],        # gets removed for ytvid type
        'tags':            request.form['tags'],
        'created_by_name': user['username'],
        'created_on':      datetime.now()
    }

    if media_type == 'movie':
        pass  # no need to add or remove attributes for movie_type

    elif media_type == 'tvshow':
        media_item['season'] = request.form['season']
        media_item['episode'] = request.form['episode']

    elif media_type == 'ytvid':
        media_item['creator'] = request.form['creator']

        del media_item['genre']
        del media_item['acts_dirs']

    media_id = media.insert_one(media_item).inserted_id

    return redirect(url_for('index_media', media=media.find(), media_id=media_id))

@media_bp.route('/<media_id>', methods=['GET'])
def show_media(media_id):
    """Returns page for just one movie,tvshow,ytvid,etc"""
    # medium = media.find_one({'_id': ObjectId(media_id)})
    # medium_reviews = reviews.find({'media_id': media_id})
    movie = tmdb.Movies(media_id).info()
    return render_template('media_show.html', movie=movie)

@media_bp.route('/<media_id>/edit', methods=['GET'])
def edit_media(media_id):
    """Returns page or form to edit media"""
    medium = media.find_one({'_id': ObjectId(media_id)})
    return render_template('media_edit.html', media=medium)


@media_bp.route('/<media_id>/update', methods=['POST'])
def update_media(media_id, user_id):
    """route to update media from edit form, goes from edit form to index OR single page?"""
    ## Should we only allow user that created movie to edit it?
    ## If so, add if statement to check user_id equals user_id attached to object
    medium = media.find_one({'_id': ObjectId(media_id)})
    media_type = medium['media_type']
    if media_type == 'movie':
        updated_media = {
            'media_type':   media_type,
            'movie_name':   'The Dark Knight',
            'genre':        'John',
            'year_created': 'Doe',
            'date_watched': 'password',
            'acts_dirs':    '',
            'tags':         '',
            'created_on':   datetime.now(),
            'created_by':   user_id
        }
    elif media_type == 'tvshow':
        updated_media = {
            'media_type':   media_type,
            'tvshow_name':  'email@gmail.com',
            'season':       'John',
            'episode':      'Doe',
            'genre':        'Doe',
            'year_created': 'password',
            'date_watched': '',
            'acts_dirs':    '',
            'tags':         '',
            'created_on':   datetime.now(),
            'created_by':   user_id
        }
    elif media_type == 'ytvid':
        updated_media = {
            'media_type':     media_type,
            'video_name':     'email@gmail.com',
            'creator':        'John',
            'date_uploaded':  'Doe',
            'date_watched':   '',
            'tags':           '',
            'created_on':     datetime.now(),
            'created_by':     user_id
        }

    media.update_one(
        {'_id': ObjectId(media_id)},
        {'$set': updated_media}
    )
    return redirect(url_for('index_media', media=media.find()))


## Maybe have this not be accessible to users? Just have them be able to remove things from their own collection
@media_bp.route('/<media_id>/delete', methods=['POST'])
def delete_media(media_id):
    """Delete media"""
    media.delete_one({'_id':ObjectId(media_id)})
    return redirect(url_for('index_media', media=media.find()))

@media_bp.route('/<media_id>/reviews', methods=['POST'])
def new_review(media_id):
    """Create new review of media, should only be on single media page"""
    review = {
        'media_id':    media_id,
        'user_id':     request.form.get('user_id'),
        'username':    request.form.get('username'),
        'movie_name':  request.form.get('movie_name'),
        'rating':      request.form.get('rating'),
        'description': request.form.get('description'),
        'date':        datetime.now(),
        'tags':        ''
    }
    reviews.insert_one(review)
    return redirect(url_for('index_media', media_id=media_id))

@media_bp.route('/<media_id>/reviews/<review_id>/delete', methods=['POST'])
def delete_review(media_id, review_id):
    reviews.delete_one({'_id': ObjectId(review_id)})
    return redirect(url_for('show_media', media_id=media_id))
    