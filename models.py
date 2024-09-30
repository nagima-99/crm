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

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    registration_date = db.Column(db.DateTime, default=datetime.now())

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

    def get_id(self):
        return str(self.id)

class Manager(User):
    __tablename__ = 'managers'
    __mapper_args__ = {'polymorphic_identity': 'manager'}
    
    birth_date = db.Column(db.DateTime, nullable=True)
    phone = db.Column(db.String(15), nullable=True)
    address = db.Column(db.String(255), nullable=True)
    main_office = db.Column(db.String(255), nullable=True)
    additional_offices = db.Column(db.String(255), nullable=True)

    def __init__(self, username, email, password, role, birth_date=None, phone=None, address=None, main_office=None, additional_offices=None):
        super().__init__(username, email, password, role)
        self.birth_date = birth_date
        self.phone = phone
        self.address = address
        self.main_office = main_office
        self.additional_offices = additional_offices

