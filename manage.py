# from flask.ext.script import Manager, prompt_bool, Shell, Server
from termcolor import colored
#
# from app import app, db
import click

from app.core import db
from app import create_app
from app.models import User, Gateway, Node, NodeInfo

import sys

app = create_app()


@app.cli.command()
def initdb():
    """ Create the SQL database. """
    db.create_all()
    print(colored('The SQL database has been created', 'green'))


@app.cli.command()
@click.confirmation_option(
    prompt='This will erase everything in the database. Do you want to continue?')
def dropdb():
    """ Delete the SQL database. """
    db.drop_all()
    print(colored('The SQL database has been deleted', 'green'))


@app.cli.command()
@click.confirmation_option(
    prompt='This will remove the current database and fill it with test data. Do you want to continue?')
def refreshdb():
    """ Fill db with test data. """
    db.drop_all()
    db.create_all()
    print(colored('The SQL database has been recreated!', 'green'))


@app.cli.command()
def testdb():
    u = User(first_name='k', last_name='b', email='test@gmail.com',
             confirmation=1, password='pass')
    db.session.add(u)
    db.session.commit()

    g1 = Gateway()
    g1.gateway_id = 'g1'
    g2 = Gateway()
    g2.gateway_id = 'g2'

    db.session.add_all([g1, g2])

    n1 = Node()
    n1.node_id = 'n1'
    n2 = Node()
    n2.node_id = 'n2'
    n3 = Node()
    n3.node_id = 'n3'

    db.session.add_all([n1, n2, n3])

    ni = NodeInfo()
    ni.lat = 123.1
    ni.long = 12.5

    ni2 = NodeInfo()
    ni2.lat = 156
    ni2.long = 167

    ni3 = NodeInfo()
    ni3.lat = 16
    ni3.long = 116

    db.session.add_all([ni, ni2, ni3])

    u.gateways.extend([g1, g2])

    g1.child_nodes.extend([n1, n2])
    g2.child_nodes.extend([n3])

    n3.node_info.extend([ni])
    n2.node_info.extend([ni2, ni3])

    db.session.commit()


@app.cli.command()
def testq():
    ni = NodeInfo.query.join(Node).filter(Node.node_id == 'n3').order_by(NodeInfo.id.desc()).first()
    print(ni.parent_node, ni.lat, ni.long, sys.stderr)


if __name__ == '__main__':
    app.cli()
