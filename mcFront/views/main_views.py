from flask import Blueprint, render_template, url_for
from werkzeug.utils import redirect
from mcFront.model import Patient, Doctor

bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/hello')
def hello_pybo():
    return 'hi pybo!!!'

@bp.route('/')
def index():
    return render_template('index.html')
