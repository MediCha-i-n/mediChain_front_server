from flask import Blueprint, url_for, render_template, flash, request, session, g
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect

from mcFront import db
from mcFront.forms import PatientUserCreateForm, DoctorUserCreateForm, PatientUserLoginForm, DoctorUserLoginForm
from mcFront.model import Patient, Doctor

import hashlib
import functools

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/signup/', methods=('GET', 'POST'))
def signup():
    form = PatientUserCreateForm()
    if request.method == 'POST' and form.validate_on_submit():
        patientUser = Patient.query.filter_by(patientName=form.patientName.data).first()
        if not patientUser:
            patientUser = Patient(patientName=form.patientName.data,
                                  password=generate_password_hash(form.password.data),
                                  patientHash=hashlib.sha256(form.patientHash.data.encode()).hexdigest()
                                  )
            db.session.add(patientUser)
            db.session.commit()
            return redirect(url_for('main.index'))
        else:
            flash('이미 존재하는 사용자 정보입니다.')
    return render_template('auth/signup.html', form=form)

@bp.route('/docSignup/', methods=('GET', 'POST'))
def docSignup():
    form = DoctorUserCreateForm()
    if request.method == 'POST' and form.validate_on_submit():
        doctorUser = Doctor.query.filter_by(doctorNumber=form.doctorNumber.data).first()
        if not doctorUser:
            doctorUser = Doctor(doctorNumber=form.doctorNumber.data,
                                doctorName=form.doctorName.data,
                                password=generate_password_hash(form.password.data))
            db.session.add(doctorUser)
            db.session.commit()
            return redirect(url_for('main.index'))
        else:
            flash('이미 존재하는 사용자 정보입니다.')
    return render_template('auth/docSignup.html', form=form)

@bp.route('/login/', methods=('GET', 'POST'))
def login():
    form = PatientUserLoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        error = None
        patientUser = Patient.query.filter_by(patientName=form.patientName.data).first()
        if not patientUser:
            error = "존재하지 않는 사용자입니다."
        elif not check_password_hash(patientUser.password, form.password.data):
            error = "틀린 비밀번호입니다."
        if error is None:
            session.clear()
            session['user_id'] = patientUser.id
            session['doc_auth'] = 0
            return redirect(url_for('main.patientMain'))
        flash(error)
    return render_template('auth/login.html', form=form)

@bp.route('/docLogin/', methods=('GET', 'POST'))
def docLogin():
    form = DoctorUserLoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        error = None
        doctorUser = Doctor.query.filter_by(doctorName=form.doctorName.data).first()
        if not doctorUser:
            error = "존재하지 않는 의사 계정입니다."
        elif not check_password_hash(doctorUser.password, form.password.data):
            error = "틀린 비밀번호입니다."
        if error is None:
            session.clear()
            session['user_id'] = doctorUser.id
            session['doc_auth'] = 1
            return redirect(url_for('main.docMain'))
        flash(error)
    return render_template('auth/docLogin.html', form=form)

@bp.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('main.index'))

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        doc_auth = session.get('doc_auth')
        if doc_auth:
            g.user = Doctor.query.get(user_id)
        else:
            g.user = Patient.query.get(user_id)
    # print(g.user.patientName)
    # print(g.user.hash)


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view

def docLogin_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None or not g.user.docAuth:
            return redirect(url_for('auth.docLogin'))
        return view(**kwargs)
    return wrapped_view

