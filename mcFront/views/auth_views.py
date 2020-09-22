from flask import Blueprint, url_for, render_template, flash, request, session
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect

from mcFront import db
from mcFront.forms import PatientUserCreateForm, DoctorUserCreateForm, PatientUserLoginForm, DoctorUserLoginForm
from mcFront.model import Patient, Doctor

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/signup/', methods=('GET', 'POST'))
def signup():
    form = PatientUserCreateForm()
    if request.method == 'POST' and form.validate_on_submit():
        patientUser = Patient.query.filter_by(patientName=form.patientName.data).first()
        if not patientUser:
            patientUser = Patient(patientName=form.patientName.data,
                                  password=generate_password_hash(form.password.data))
            db.session.add(patientUser)
            db.session.commit()
            return redirect(url_for('main.index'))
        else:
            flash('이미 존재하는 사용자입니다.')
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
            flash('이미 존재하는 사용자입니다.')
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
            session['patient_id'] = patientUser.id
            return redirect(url_for('main.index'))
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
            session['doctor_id'] = doctorUser.id
            return redirect(url_for('main.index'))
        flash(error)
    return render_template('auth/docLogin.html', form=form)
