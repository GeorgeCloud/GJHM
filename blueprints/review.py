from flask import Blueprint, render_template, request, redirect, url_for
from datetime import datetime
from bson.objectid import ObjectId
from db import *

reviews_bp = Blueprint('reviews_bp', __name__)

@reviews_bp.route('/', methods=['GET'])
def index_reviews():
    