from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.sql import func

from flask_login import UserMixin

from .core import db, bcrypt


class User(db.Model, UserMixin):
    """ A user who has an account on the website. """

    def __init__(self, first_name, last_name, email, confirmation, password):
        self.first_name = first_name,
        self.last_name = last_name,
        self.email = email,
        self.confirmation = confirmation,
        self._password = password

    __tablename__ = 'users'

    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    email = db.Column(db.String, primary_key=True)
    confirmation = db.Column(db.Boolean)
    _password = db.Column(db.String)

    @property
    def full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def _set_password(self, plaintext):
        self._password = bcrypt.generate_password_hash(plaintext)

    def check_password(self, plaintext):
        return bcrypt.check_password_hash(self.password, plaintext)

    def get_id(self):
        return self.email


# class AuthorizedClients(db.Model):
#
#     """ A client which is authorized to use the webhook system """
#
#     __tablename__ = 'authorized_clients'
#
#     client_ip = db.Column(db.String, primary_key=True)
#     pub_time = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
#
#     @property
#     def ip(self):
#         return '{}'.format(self.client_ip)
