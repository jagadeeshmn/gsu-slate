import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'very-secure-key'
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/mkoritala1'
    SQLALCHEMY_TRACK_MODIFICATIONS = False