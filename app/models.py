from flask_login import UserMixin

from .core import db, bcrypt

import datetime
import uuid


class User(db.Model, UserMixin):

    def __init__(self, first_name, last_name, email, password, confirmation=0):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.confirmation = confirmation
        self.password_hash = bcrypt.generate_password_hash(password)
        self.registered_on = datetime.datetime.now()
        self.token = self.set_token()

    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    confirmation = db.Column(db.Integer)
    password_hash = db.Column(db.String)
    registered_on = db.Column(db.DateTime, nullable=False)
    token = db.Column(db.String)

    def set_token(self):
        return str(uuid.uuid4())

    @property
    def full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)

    def check_password(self, plaintext):
        return bcrypt.check_password_hash(self.password_hash, plaintext)

    def get_id(self):
        return self.id
