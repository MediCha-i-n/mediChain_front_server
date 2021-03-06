from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, IntegerField
from wtforms.validators import DataRequired, Length, EqualTo

class PatientUserCreateForm(FlaskForm):
    patientName = StringField('사용자 이름', validators=[DataRequired(), Length(min=2, max=50)])
    password = PasswordField('비밀번호', validators=[
        DataRequired(), EqualTo('passwordChker', '비밀번호가 일치하지 않습니다.')
    ])
    passwordChker = PasswordField('비밀 번호 확인', validators=[DataRequired()])
    patientHash = StringField('환자 해쉬', validators=[DataRequired(), Length(13)])

class DoctorUserCreateForm(FlaskForm):
    doctorNumber = StringField('의사 번호', validators=[DataRequired()])
    doctorName = StringField('사용자 이름', validators=[DataRequired(), Length(min=2, max=50)])
    password = PasswordField('비밀번호', validators=[
        DataRequired(), EqualTo('passwordChker', '비밀번호가 일치하지 않습니다.')
    ])
    passwordChker = PasswordField('비밀 번호 확인', validators=[DataRequired()])

class PatientUserLoginForm(FlaskForm):
    patientName = StringField('사용자 이름', validators=[DataRequired(), Length(min=2, max=50)])
    password = PasswordField('비밀번호', validators=[DataRequired()])

class DoctorUserLoginForm(FlaskForm):
    doctorName = StringField('사용자 이름', validators=[DataRequired(), Length(min=2, max=50)])
    password = PasswordField('비밀번호', validators=[DataRequired()])

class ActUploadForm(FlaskForm):
    image = StringField('image', validators=[DataRequired()])
    patientHash = StringField('patientHash', validators=[DataRequired()])

class ActSearchForm(FlaskForm):
    patientHash = StringField('patientHash', validators=[DataRequired()])
