from flask import Blueprint, render_template, request
from datetime import datetime
# from app import media

media_bp = Blueprint('media_bp', __name__)

@media_bp.route('/', methods=['GET'])
def index_users():
    # Returns all movies
    return render_template('index.html')

@media_bp.route('/create', methods=['POST'])
def create_movie():
    form_name = request.form['form-name']
    if form_name == 'movie':
        movie = {
            'movie_name':   'The Dark Knight',
            'genre':        'John',
            'year_created': 'Doe',
            'date_watched': 'password',
            'acts_dirs':    '',
            'tags':         '',
            'created_on':   datetime.now()
            #should date watched and date uploaded by the same?
        }

        media_id = media.insert_one(movie).inserted_id

    elif form_name == 'tvshow':
        tvshow = {
            'tvshow_name':      'email@gmail.com',
            'season': 'John',
            'episode':  'Doe',
            'genre':  'Doe',
            'year_created':   'password',
            'date_watched': '',
            'acts_dirs':    '',
            'tags':         '',
            'created_on': datetime.now(),
        }

        media_id = media.insert_one(tvshow).inserted_id

    elif form_name == 'ytvid':
        ytvid = {
            'video_name':     'email@gmail.com',
            'creator':        'John',
            'date_uploaded':  'Doe',
            'date_watched':   '',
            'tags':           '',
            'created_on':     datetime.now(),
        }

        media_id = media.insert_one(ytvid).inserted_id

    return render_template('show_media.html', media_id=media_id)

@media_bp.route('/edit', methods=['GET'])
def edit_media():
    pass

@media_bp.route('/update', methods=['POST'])
def update_media():
    pass

@media_bp.route('/delete', methods=['POST'])
def delete_media():
    pass