from flask import Blueprint, render_template, url_for, g
from werkzeug.utils import redirect
import subprocess

from mcFront import db
from mcFront.model import Patient, Doctor

bp = Blueprint('act', __name__, url_prefix='/act')

@bp.route('/search/<String:hash>', methods=('GET', 'POST'))
@login_required
def search(hash):
    pass

@bp.route('/upload/<String:image>', methods=('GET', 'POST'))
@docLogin_required
def upload(image):
    pass
