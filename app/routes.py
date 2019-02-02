from flask import request, flash, jsonify
from app import app, db
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import Applicant, Application, Program
from flask_api import status
from datetime import datetime
from sqlalchemy import func

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
            return jsonify({'status': status.HTTP_401_UNAUTHORIZED,'message':'Invalid Credentials'})
        else:
            return jsonify({'status': status.HTTP_200_OK,'message':'Login successful','aid':applicant.aid})
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
            return jsonify({'status': status.HTTP_409_CONFLICT,'message':'Please use a different email'})
    except:
        return jsonify({'status': status.HTTP_500_INTERNAL_SERVER_ERROR,'message':'Unable to register'})

@app.route('/edit_profile',methods=['POST'])
def edit_profile():
    try:
        applicant = Applicant.query.filter_by(aid = request.json['aid']).first()
        if applicant is not None:
            applicant.fname = request.json['fname']
            applicant.lname = request.json['lname']
            if 'password' in request.json.keys():
                password = hash_password(request.json['password'])
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

            return jsonify({'status': status.HTTP_200_OK,'message':'Your profile updated successfully'})
        else:
            return jsonify({'status': status.HTTP_404_NOT_FOUND,'message':'Applicant Not found'})
    except Exception as e:
        return jsonify({'status': status.HTTP_500_INTERNAL_SERVER_ERROR,'message':str(e)})
        # return jsonify({'status': status.HTTP_500_INTERNAL_SERVER_ERROR,'message':'Unable to Edit Profile'})

@app.route('/apply',methods=['POST'])
def apply():
    try:
        applicant = Applicant.query.filter_by(aid = request.json['aid']).first()
        if applicant is not None:
            application = Application.query.filter_by(email = applicant.email).first()
            if application is None:
                program = Program.query.filter_by(program = request.json['program']).first()
                application = Application(
                    email = applicant.email,
                    university = 'GSU',
                    dname = request.json['dname'],
                    program = program.program,
                    dateOfApp = datetime.utcnow(),
                    termOfAdmission = request.json['termOfAdmission'],
                    yearOfAdmission = request.json['yearOfAdmission'],
                    admissionStatus = 'PENDING',
                    dataSentToPaws = 'NO',
                    applicant_email = applicant.email,
                    applicant_program = program.program
                )

                db.session.add(application)
                db.session.commit()

                return jsonify({'status': status.HTTP_201_CREATED,'message':'Your application sent successfully'})
            else:
                return jsonify({'status': status.HTTP_200_OK,'message':'Looks like you have already applied.'})
        else:
            return jsonify({'status':status.HTTP_404_NOT_FOUND,'message':'Applicant not found'})
    except Exception as e:
        return jsonify({'status':status.HTTP_500_INTERNAL_SERVER_ERROR,'message':str(e)})
        # return jsonify({'status':status.HTTP_500_INTERNAL_SERVER_ERROR,'message':'Unable to apply'})

@app.route('/update_status',methods=['PUT'])
def update_status():
    try:
        application = Application.query.filter_by(email = request.json['email']).first()
        if application is not None:
            application.admissionStatus = request.json['admissionStatus']
            
            db.session.add(application)
            db.session.commit()

            return jsonify({'status': status.HTTP_201_CREATED,'message':'Application status updated'})
        else:
            return jsonify({'status':status.HTTP_200_OK,'message':'Application not found'})
    except:
        return jsonify({'status':status.HTTP_500_INTERNAL_SERVER_ERROR,'message':'Unable to change status'})

@app.route('/get_accepted_applications',methods=['GET'])        
def get_accepted_applications():     
    try:
        return_data = []
        applications = db.session.query(Applicant,Application).filter(Applicant.email == Application.email).filter(Application.admissionStatus == 'ACCEPT',Application.university == 'GSU').add_columns(Application.email,Applicant.fname,Applicant.lname,Application.dateOfApp).all()
        if applications is not None:
            for application in applications:
                application_data = {}
                application_data['email'] = application[2]
                application_data['fname'] = application[3]
                application_data['lname'] = application[4]
                application_data['dateOfApp'] = application[5]
                return_data.append(application_data)
            return jsonify({'status':status.HTTP_200_OK,'data':return_data})
    except Exception as e:
        return jsonify({'status':status.HTTP_500_INTERNAL_SERVER_ERROR,'message':str(e)})
        # return jsonify({'status':status.HTTP_500_INTERNAL_SERVER_ERROR,'message':'Unable to get applications'})

@app.route('/get_all_applications',methods=['GET'])        
def get_all_applications():     
    try:
        return_data = []
        applications = db.session.query(Applicant,Application).filter(Applicant.email == Application.email).filter(Application.university == 'GSU').add_columns(Application.email,Applicant.aid,Applicant.fname,Applicant.lname,Application.dateOfApp,Application.admissionStatus).all()
        if applications is not None:
            for application in applications:
                application_data = {}
                application_data['email'] = application[2]
                application_data['aid'] = application[3]
                application_data['fname'] = application[4]
                application_data['lname'] = application[5]
                application_data['dateOfApp'] = application[6]
                application_data['admissionStatus'] = application[7]
                return_data.append(application_data)
            return jsonify({'status':status.HTTP_200_OK,'data':return_data})
    except Exception as e:
        return jsonify({'status':status.HTTP_500_INTERNAL_SERVER_ERROR,'message':str(e)})
        # return jsonify({'status':status.HTTP_500_INTERNAL_SERVER_ERROR,'message':'Unable to get applications'})

@app.route('/<applicantID>/fetch_profile',methods=['GET'])
def fetch_profile(applicantID):
    try:
        applicant = Applicant.query.filter_by(aid = applicantID).first()
        return_data = {}
        if applicant is not None:
            return_data['email'] = applicant.email
            return_data['fname'] = applicant.fname
            return_data['lname'] = applicant.lname
            return_data['address1'] = applicant.address1
            return_data['address2'] = applicant.address2
            return_data['city'] = applicant.city
            return_data['state'] = applicant.state
            return_data['zip'] = applicant.zip
            return_data['GREQ'] = applicant.GREQ
            return_data['GREV'] = applicant.GREV
            return_data['GREA'] = applicant.GREA
            return_data['TOEFL'] = applicant.TOEFL
            return jsonify({'status':status.HTTP_200_OK,'data':return_data})
        else:
            return jsonify({'status':status.HTTP_200_OK,'message':'Applicant not found'})
    except:
        return jsonify({'status':status.HTTP_500_INTERNAL_SERVER_ERROR,'message':'Unable to fetch Applicant profile'})

@app.route('/<applicantID>/fetch_application',methods=['GET'])
def fetch_application(applicantID):
    try:
        application = db.session.query(Applicant,Application).filter(Applicant.email == Application.email).filter(Applicant.aid == applicantID).first()
        return_data = {}
        if application is not None:
            return_data['email'] = application.Applicant.email
            return_data['fname'] = application.Applicant.fname
            return_data['lname'] = application.Applicant.lname
            return_data['address1'] = application.Applicant.address1
            return_data['address2'] = application.Applicant.address2
            return_data['city'] = application.Applicant.city
            return_data['state'] = application.Applicant.state
            return_data['zip'] = application.Applicant.zip
            return_data['GREQ'] = application.Applicant.GREQ
            return_data['GREV'] = application.Applicant.GREV
            return_data['GREA'] = application.Applicant.GREA
            return_data['TOEFL'] = application.Applicant.TOEFL
            return_data['university'] = application.Application.university
            return_data['dname'] = application.Application.dname
            return_data['program'] = application.Application.program
            return_data['dateOfApp'] = application.Application.dateOfApp
            return_data['termOfAdmission'] = application.Application.termOfAdmission
            return_data['yearOfAdmission'] = application.Application.yearOfAdmission
            return_data['admissionStatus'] = application.Application.admissionStatus
            return jsonify({'status':status.HTTP_200_OK,'data':return_data})
        else:
            return jsonify({'status':status.HTTP_200_OK,'message':'Application not found'})
    except:
        return jsonify({'status':status.HTTP_500_INTERNAL_SERVER_ERROR,'message':'Unable to fetch Application'})


@app.route('/getstats',methods=['POST'])        
def getstats():       
    try:
        university = request.json['university']
        termOfAdmission= request.json['termOfAdmission']
        yearOfAdmission=request.json['yearOfAdmission']
        #return_data = []
        statistics = db.session.query(Application.dname,Application.program,Application.admissionStatus, func.count(Application.admissionStatus).label('Count of Status')).filter(Application.university == university, Application.termOfAdmission == termOfAdmission , Application.yearOfAdmission == yearOfAdmission).group_by(Application.dname,Application.program,Application.admissionStatus).all()
        if statistics is not None:
            def fill_dict(p,v,total,total_department):
                course = v.pop(0)
                if course not in p:
                  total = 0  
                  num = {}
                  num[v[0]]=v[1] 
                  p[course]=num 
                else:  
                  p[course][v[0]] = v[1]
                  
                total+=int(v[1])
                total_department+=int(v[1])
                p[course]['total_'+course]=total
                return p,total,total_department
                 
            d = {}
            total_program = 0
            total_department = 0
            print(statistics) 
            for k, *v in statistics:
                if k not in d:
                  p={}  
                  total_department = 0
                  d[k]=p
                  d[k]['total_department']=total_department
                p,total_program,total_department = fill_dict(p,v,total_program,total_department)
                d[k]['total_department']=total_department 

            return jsonify({'status':status.HTTP_200_OK,'data':d})
    except Exception as e:
        return jsonify({'status':status.HTTP_500_INTERNAL_SERVER_ERROR,'message':str(e)})
        # return jsonify({'status':status.HTTP_500_INTERNAL_SERVER_ERROR,'message':'Unable to get applications'})

