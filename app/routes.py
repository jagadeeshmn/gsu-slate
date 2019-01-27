from flask import request, flash, jsonify
from app import app, db
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import Applicant
from flask_api import status

def hash_password(password):
    return generate_password_hash(password)

def check_password(password,password_hash):
    return check_password_hash(password,password_hash)

@app.route('/')
@app.route('/index')
def index():
    return "Hello world"

@app.route('/login',methods=['POST'])
def login():
    try:
        applicant = Applicant.query.filter_by(email = request.json['email']).first()
        if applicant is None or not check_password(applicant.password,request.json['password']):
            return jsonify({'status': status.HTTP_200_OK,'message':'Invalid Credentials'})
        else:
            return jsonify({'status': status.HTTP_200_OK,'message':'Login successful'})
    except:
        return jsonify({'status': status.HTTP_500_INTERNAL_SERVER_ERROR,'message':'Unable to login'})

@app.route('/register',methods=['POST'])
def register():
    try:
        applicant = Applicant.query.filter_by(email = request.json['email']).first()
        if applicant is None:
            password = hash_password(request.json['password'])
            applicant = Applicant(email=request.json['email'],fname=request.json['fname'],lname=request.json['lname'],password=password)
            db.session.add(applicant)
            db.session.commit()
            return jsonify({'status': status.HTTP_201_CREATED,'message':'Congratulations, you are now a registered user'})
        else:
            return jsonify({'status': status.HTTP_200_OK,'message':'Please use a different email'})
    except:
        return jsonify({'status': status.HTTP_500_INTERNAL_SERVER_ERROR,'message':'Unable to register'})

@app.route('/edit_profile',methods=['POST'])
def edit_profile():
    try:
        applicant = Applicant.query.filter_by(email = request.json['email']).first()
        if applicant is not None:
            password = hash_password(request.json['password'])
            
            applicant.fname = request.json['fname']
            applicant.lname = request.json['lname']
            applicant.password = password
            applicant.address1 = request.json['address1']
            applicant.address2 = request.json['address2']
            applicant.city = request.json['city']
            applicant.state = request.json['state']
            applicant.zip = int(request.json['zip'])
            applicant.GREQ = int(request.json['GREQ'])
            applicant.GREV = int(request.json['GREV'])
            applicant.GREA = float(request.json['GREA'])
            applicant.TOEFL = int(request.json['TOEFL'])

            db.session.add(applicant)
            db.session.commit()

            return jsonify({'status': status.HTTP_201_CREATED,'message':'Your profile updated successfully'})
        else:
            return jsonify({'status': status.HTTP_200_OK,'message':'Applicant Not found'})
    except:
        return jsonify({'status': status.HTTP_500_INTERNAL_SERVER_ERROR,'message':'Unable to Edit Profile'})

@app.route('/apply',methods=['POST'])
def apply():
    try:
        pass
    except:
        return jsonify({'status':status.HTTP_500_INTERNAL_SERVER_ERROR,'message':'Unable to apply'})