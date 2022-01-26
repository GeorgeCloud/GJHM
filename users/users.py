from flask import Blueprint, render_template

users_bp = Blueprint('users_bp', __name__)

@users_bp.route('/', methods=['GET'])
def index_users():
    return render_template('index.html')

@users_bp.route('/new', methods=['GET'])
def new_user():
    return 'new user\'s page'

@users_bp.route('/create', methods=['POST'])
def create_user():
    return 'user created!'

@users_bp.route('/edit', methods=['GET'])
def edit_user():
    pass

@users_bp.route('/update', methods=['POST'])
def update_user():
    pass
