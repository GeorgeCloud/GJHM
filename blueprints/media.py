from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from extensions import is_authenticated, user_playlists, login_required
from datetime import datetime
import tmdbsimple as tmdb
from db import *
import uuid

media_bp = Blueprint('media_bp', __name__, template_folder='templates')
api_search = tmdb.Search()

@media_bp.route('/', methods=['GET'])
def index_media():
    """Return ALL media"""
    popular_media = tmdb.Movies().popular()['results']
    return render_template('media_index.html', media=popular_media)

@media_bp.route('/reviews', methods=['GET'])
def index_reviews():
    """Return ALL reviews"""
    all_reviews = reviews.find({})
    return render_template('reviews_index.html', reviews=all_reviews)

@media_bp.route('/create', methods=['POST'])
@login_required
def new_movie(user_id):
    """Creates new media to db"""
    user = users.find_one({'_id': user_id})
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

@media_bp.route('/<media_id>/reviews', methods=['POST'])
def new_review(media_id):
    """Create new review of media, should only be on single media page"""
    review = {
        '_id':         uuid.uuid4().hex,
        'title':       request.form.get('title'),
        'rating':      request.form.get('rating'),
        'description': request.form.get('description'),
        'username':    request.form.get('username'),
        'user_id':     request.form.get('user_id'),
        'media_id':    media_id,
        'created_on':  datetime.now(),
        'tags':        ''
    }
    reviews.insert_one(review)
    flash('Successfully Review Created.')
    return redirect(url_for('media_bp.show_media', media_id=media_id))

@media_bp.route('/search', methods=['GET', 'POST'])
def search_media():
    if request.method == 'GET':
        return render_template('media_search.html')

    search_query = request.form['search_query']
    #
    # m_result =
    # u_result =
    # p_result =
    user_lists = None

    if is_authenticated():
        user_lists = list(user_playlists(session['current_user']['_id']))

    return render_template('media_search.html',
                           search_query    = search_query,
                           media_result    = api_search.multi(query=search_query)['results'][:3],
                           user_result     = users.find({'username': search_query})[:3],
                           playlist_result = playlists.find({'title': search_query})[:3],
                           user_playlists  = user_lists if user_lists else None
                           )

@media_bp.route('/<media_id>/reviews', methods=['GET'])
def show_media(media_id):
    single_media = tmdb.Movies(media_id).info()
    media_reviews = reviews.find({'media_id': media_id})

    return render_template('media_show.html', media=single_media, reviews=media_reviews, users=users)

@media_bp.route('/<media_id>/reviews/<review_id>/delete', methods=['POST'])
def delete_review(media_id, review_id):
    reviews.delete_one({'_id': review_id})
    flash('Successfully Deleted Review.')
    return redirect(url_for('media_bp.show_media', media_id=media_id))
