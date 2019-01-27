from app import db
from datetime import datetime

class Department(db.Model):
    university = db.Column(db.String(40),nullable=False)
    dname = db.Column(db.String(40),primary_key=True)
    programs = db.relationship('Program',backref='department',lazy='dynamic')

    def __repr__(self):
        return '<Department {}>'.format(self.dname)

class Program(db.Model):
    university = db.Column(db.String(40),nullable=False)
    dname = db.Column(db.String(40),nullable=False)
    program = db.Column(db.String(10), db.CheckConstraint('program in (MS,PhD)'),primary_key=True)
    department_dname = db.Column(db.String(40), db.ForeignKey('department.dname'))
    applications = db.relationship('Application',backref='application',lazy='dynamic')

    def __repr__(self):
        return '<Program {}>'.format(self.program)

class Applicant(db.Model):
    aid = db.Column(db.Integer,db.Sequence('applicant_aid_seq'),db.CheckConstraint('aid > 999 and sid<10000'),unique=True)
    email = db.Column(db.String(40),primary_key=True)
    password = db.Column(db.String(128),nullable=False)
    fname = db.Column(db.String(20),nullable=False)
    lname = db.Column(db.String(20),nullable=False)
    address1 = db.Column(db.String(40))
    address2 = db.Column(db.String(40))
    city = db.Column(db.String(40))
    state = db.Column(db.String(40))
    zip = db.Column(db.Integer)
    GREQ = db.Column(db.Integer)
    GREV = db.Column(db.Integer)
    GREA = db.Column(db.Float)
    TOEFL = db.Column(db.Integer)
    applications = db.relationship('Application',backref='applied',lazy='dynamic')

    def __repr__(self):
        return '<Application {}>'.format(self.email)

class Application(db.Model):
    email = db.Column(db.String(40),primary_key=True)
    university = db.Column(db.String(40),nullable=False)
    dname = db.Column(db.String(20),nullable=False)
    program = db.Column(db.String(10),db.CheckConstraint('program in (MS,PhD)'),nullable=False)
    dateOfApp = db.Column(db.DateTime, default=datetime.utcnow)
    termOfAdmission = db.Column(db.String(2),db.CheckConstraint('termOfAdmission in (FA,SP,SU)'),nullable=True)
    yearOfAdmission = db.Column(db.Integer,db.CheckConstraint('yearOfAdmission > 1999 and yearOfAdmission<2100'),nullable=True)
    admissionStatus = db.Column(db.String(10),db.CheckConstraint('admissionStatus in (ACCEPT,REJECT,PENDING)'))
    dataSentToPaws = db.Column(db.String(3),db.CheckConstraint('dataSentToPaws in (YES,NO)'))
    applicant_email = db.Column(db.String(40),db.ForeignKey('applicant.email'))
    applicant_program = db.Column(db.String(40),db.ForeignKey('program.program'))

    def __repr__(self):
        return '<Application {}>'.format(self.email)
