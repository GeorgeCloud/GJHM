from flask import Blueprint, render_template, request, redirect, url_for
from datetime import datetime
from bson.objectid import ObjectId
from app import media

media_bp = Blueprint('media_bp', __name__)

@media_bp.route('/', methods=['GET'])
def index_media():
    # Returns all movies
    return render_template('show_media.html', media=media.find())


@media_bp.route('/create', methods=['POST'])
def create_movie(user_id):
    form_name = request.form['form-name']
    if form_name == 'movie':
        movie = {
            'media_type':   form_name,
            'movie_name':   'The Dark Knight',
            'genre':        'John',
            'year_created': 'Doe',
            'date_watched': 'password',
            'acts_dirs':    '',
            'tags':         '',
            'created_on':   datetime.now(),
            'created_by':   user_id
            #should date watched and date uploaded by the same?
        }

        media_id = media.insert_one(movie).inserted_id

    elif form_name == 'tvshow':
        tvshow = {
            'media_type':   form_name,
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

        media_id = media.insert_one(tvshow).inserted_id

    elif form_name == 'ytvid':
        ytvid = {
            'media_type':     form_name,
            'video_name':     'email@gmail.com',
            'creator':        'John',
            'date_uploaded':  'Doe',
            'date_watched':   '',
            'tags':           '',
            'created_on':     datetime.now(),
            'created_by':     user_id
        }

        media_id = media.insert_one(ytvid).inserted_id

    return redirect(url_for('index_media', media=media.find(), media_id=media_id))


@media_bp.route('/edit/<media_id>', methods=['GET'])
def edit_media(media_id):
    medium = media.find_one({'_id': ObjectId(media_id)})
    return render_template('media_edit.html', media=medium)


@media_bp.route('/update/<media_id>', methods=['POST'])
def update_media(media_id, user_id):
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
        {'$set':updated_media}
    )
    return redirect(url_for('index_media', media=media.find()))


## Maybe have this not be accessible to users? Just have them be able to remove things from their own collection
@media_bp.route('/delete/<media_id>', methods=['POST'])
def delete_media(media_id):
    media.delete_one({'_id':ObjectId(media_id)})
    return redirect(url_for('index_media', media=media.find()))