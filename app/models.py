from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

from itsdangerous import Serializer

from flask_login import UserMixin
from flask import current_app

from .core import db, bcrypt

import datetime
import uuid
import sys


class User(db.Model, UserMixin):

    def __init__(self, first_name, last_name, email, password, confirmation=0):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.confirmation = confirmation
        self.password_hash = bcrypt.generate_password_hash(password)
        self.registered_on = datetime.datetime.now()
        self.set_token()

    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    confirmation = db.Column(db.Integer)
    password_hash = db.Column(db.String)
    registered_on = db.Column(db.DateTime, nullable=False)
    _token = db.Column(db.String)

    # def __init__(self, first_name, last_name, email, password, confirmation=0):
    #     self.first_name = first_name
    #     self.last_name = last_name
    #     self.email = email
    #     self.confirmation = confirmation
    #     self._password = password
    #     self.registered_on = datetime.datetime.now()
    #     self.set_token()

    gateways = relationship('Gateway', backref='user', cascade='all, delete-orphan')

    def set_token(self):
        self._token = str(uuid.uuid4())
        return self.token

    @hybrid_property
    def token(self):
        return self._token

    @property
    def full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)

    # @hybrid_property
    # def password_hash(self):
    #     return self.password_hash
    #
    # @password_hash.setter
    # def password_hash(self, plaintext):
    #     self.password_hash = bcrypt.generate_password_hash(plaintext)

    def check_password(self, plaintext):
        return bcrypt.check_password_hash(self.password_hash, plaintext)

    def get_id(self):
        return self.id

    def get_node(self, id):
        nodes = [n for g in self.gateways for n in g.child_nodes]
        for n in nodes:
            print(n.node_id, sys.stderr)
            if n.node_id == id:
                return n


class Gateway(db.Model):

    __tablename__ = 'gateway'

    id = db.Column(db.Integer, primary_key=True)
    gateway_id = db.Column(db.String)

    owner = db.Column(db.Integer, db.ForeignKey('user.id'))
    child_nodes = relationship('Node', backref='gateway', cascade='all, delete-orphan')


class Node(db.Model):

    __tablename__ = 'node'

    id = db.Column(db.Integer, primary_key=True)
    node_id = db.Column(db.String)

    parent_gateway = db.Column(db.Integer, db.ForeignKey('gateway.id'))
    node_info = relationship('NodeInfo', backref='node', cascade='all, delete-orphan')


class NodeInfo(db.Model):

    __tablename__ = 'location'

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.Integer)
    lat = db.Column(db.Float)
    long = db.Column(db.Float)
    status = db.Column(db.Integer)

    parent_node = db.Column(db.Integer, db.ForeignKey('node.id'))

# u = User('k', 'b', 'kylebowman99@gmail.com', True, 'lol')
#
# g = Gateway()
# g.gateway_id = 'g1'
# db.session.add(g)
#
# n = Node()
# n.node_id = 'n1'
# db.session.add(n)
#
# ni = NodeInfo()
# ni.lat = 123.1
# ni.long = 12.5
# db.session.add(ni)
#
# db.session.commit()
#
# g.child_nodes = n
#
# n.node_info = ni
#
# hello = Gateway.query.filter_by(gateway_id='g1').first()
# print(hello, sys.stderr)
# print("ok", sys.stderr)

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
