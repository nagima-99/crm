from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, current_app
from flask_login import UserMixin
from datetime import datetime
from flask_migrate import Migrate


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '00cb48ff0bb190c58724e6b3834ced90'


'''
для загрузки переменных окружения из файла .env (временно закомментирован)

import os
from dotenv import load_dotenv # библиотека для работы с переменными окружения

# Загрузка переменных из .env файла
load_dotenv()
app = Flask(__name__)

# переменные окружения
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
'''

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    registration_date = db.Column(db.DateTime, default=datetime.now())
    __mapper_args__ = {
        'polymorphic_identity': 'user',  # базовый класс
        'polymorphic_on': role            # поле, по которому SQLAlchemy будет различать типы пользователей
    }

    def __init__(self, username, email, password, role):
        self.username = username
        self.email = email
        self.set_password(password)
        self.role = role
        self.registration_date = datetime.now()

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Administrator(User):
    __tablename__ = 'administrators'
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)

    
    birth_date = db.Column(db.Date)
    phone = db.Column(db.String(15), nullable=True)
    address = db.Column(db.String(255), nullable=True)
    main_office = db.Column(db.String(255), nullable=True)
    additional_offices = db.Column(db.String(255), nullable=True)

    __mapper_args__ = {
        'polymorphic_identity': 'Администратор',
    }

    def __init__(self, username, email, password, birth_date=None, phone=None, address=None, main_office=None, additional_offices=None):
        super().__init__(username, email, password, role='Администратор')
        self.birth_date = birth_date
        self.phone = phone
        self.address = address
        self.main_office = main_office
        self.additional_offices = additional_offices

class Student(User):
    __tablename__ = 'students'
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    
    birth_date = db.Column(db.Date, nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    address = db.Column(db.String(255), nullable=True)
    
    client_name = db.Column(db.String(255), nullable=True)
    client_relation = db.Column(db.String(100), nullable=True)
    client_phone = db.Column(db.String(20), nullable=True)
    client_workplace = db.Column(db.String(255), nullable=True)
    client_position = db.Column(db.String(100), nullable=True)

    __mapper_args__ = {
        'polymorphic_identity': 'student',
    }

    def __init__(self, username, email, password, birth_date=None, phone=None, address=None, client_name=None, client_relation=None, client_phone=None, client_workplace=None, client_position=None):
        super().__init__(username, email, password, role='student')
        self.birth_date = birth_date
        self.phone = phone
        self.address = address
        self.client_name = client_name
        self.client_relation = client_relation
        self.client_phone = client_phone
        self.client_workplace = client_workplace
        self.client_position = client_position
