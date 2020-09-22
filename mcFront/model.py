from mcFront import db

class Patient(db.Model):
    # id is only needed in db
    id = db.Column(db.Integer, primary_key=True)
    # patientName is used for sign in
    patientName = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    docAuth = db.Column(db.Integer, nullable=False, server_default='0')

class Doctor(db.Model):
    # id is only needed in db
    id = db.Column(db.Integer, primary_key=True)
    doctorNumber = db.Column(db.String(300), unique=True, nullable=False)
    doctorName = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    docAuth = db.Column(db.Integer, nullable=False, server_default='1')
