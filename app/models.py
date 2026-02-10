from . import db
from sqlalchemy import Enum
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password_hash = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    
class Driver(db.Model):
    __tablename__ = 'drivers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000))
    old = db.Column(Enum("25", "26", "27", "28", "29", "30", "31", "32"))
    jenre = db.Column(db.String(1000))
    capacity = db.Column(db.Integer)

class CheckedDriver(db.Model):
    __tablename__ = 'checked_drivers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000))
    old = db.Column(Enum("25", "26", "27", "28", "29", "30", "31", "32"))
    jenre = db.Column(Enum("HIPHOP", "BREAK", "LOCK", "POP", "JAZZ", "WAACK", "HOUSE"))
    section = db.Column(Enum("1", "2", "3"))
    rehersal = db.Column(Enum("1","2"))
    capacity = db.Column(db.Integer)

class Passenger(db.Model):
    __tablename__ = 'passengers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000))
    old = db.Column(Enum("25", "26", "27", "28", "29", "30", "31", "32"))
    jenre = db.Column(Enum("HIPHOP", "BREAK", "LOCK", "POP", "JAZZ", "WAACK", "HOUSE"))

class CheckedPassenger(db.Model):
    __tablename__ = 'checked_passengers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000))
    old = db.Column(Enum("25", "26", "27", "28", "29", "30", "31", "32"))
    section = db.Column(Enum("1", "2", "3"))
    rehersal = db.Column(Enum("1","2"))
    jenre = db.Column(db.String(1000))

class Log_History(db.Model):
    __tablename__ = 'log_history'
    id = db.Column(db.Integer, primary_key=True)
    driver_name = db.Column(db.String(1000))
    passenger_name = db.Column(db.String(1000))

class History(db.Model):
    __tablename__ = 'history' 
    id = db.Column(db.Integer, primary_key=True)
    history_name = db.Column(db.String(1000))
    driver_name = db.Column(db.String(1000))
    passenger_name = db.Column(db.String(1000))
    created_date = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)

