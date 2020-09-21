from mcFront import db

class Patient(db.Model):
    # id is only needed in db
    id = db.Column(db.Integer, primary_key=True)
    # patientName is Patient's Hash
    patientName = db.Column(db.String(300), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

class Doctor(db.Model):
    # id is only needed in db
    id = db.Column(db.Integer, primary_key=True)
    # doctorName is doctor's unique number
    doctorName = db.Column(db.String(300), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)