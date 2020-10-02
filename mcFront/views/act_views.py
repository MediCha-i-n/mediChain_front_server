from flask import Blueprint, request, render_template, url_for, g
from werkzeug.utils import redirect
from werkzeug.datastructures import FileStorage
import subprocess
import base64

from mcFront import db
from mcFront.model import Patient, Doctor
from mcFront.forms import ActSearchForm, ActUploadForm
from ..views.auth_views import login_required, docLogin_required

bp = Blueprint('act', __name__, url_prefix='/act')

@bp.route('/search/', methods=('GET','POST'))
@login_required
def search():
    form = ActSearchForm()
    if request.method == 'POST' and form.validate_on_submit():
        hash = form.hash.data
        print(hash)
        # return hash
    return render_template('act/search.html', form=form)

@bp.route('/upload/', methods=('GET','POST'))
@docLogin_required
def upload():
    form = ActUploadForm()
    if request.method == 'POST' and form.validate_on_submit():
        image = form.image.data
        # image_length = image.content_length   #   This is 0.
        image_file = image.read()
        encoded_file = base64.b64encode(image_file)

    return render_template('act/upload.html', form=form)

