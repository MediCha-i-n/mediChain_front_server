from flask import Blueprint, request, render_template, url_for, g
from werkzeug.utils import redirect
import subprocess

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
        return hash
    return render_template('act/search.html', form=form)

@bp.route('/upload/', methods=('GET','POST'))
@docLogin_required
def upload():
    form = ActUploadForm()
    if request.method == 'POST' and form.validate_on_submit():
        image = form.image.data
        print(image)

        # return image
    return render_template('act/upload.html', form=form)

