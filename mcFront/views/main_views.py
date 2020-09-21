from flask import Blueprint, render_template

from mcFront.model import Patient, Doctor

bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/hello')
def hello_pybo():
    return 'hi pybo!!!'

@bp.route('/')
def index():
    return 'this works well'