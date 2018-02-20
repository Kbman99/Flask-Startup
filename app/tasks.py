import sys
from app.models import User, NodeInfo
from .core import scheduler, db
from faker import Faker
import random
import time

fake = Faker()


def grab_user():
    user = User.query.filter(User.email == 'test@gmail.com').first()
    return user


def generate_coords():
    with scheduler.app.app_context():
        u = grab_user()
        nodes = [n for g in u.gateways for n in g.child_nodes]

        state_coords = [[32, -86], [39, -86], [37, -119], [42, -71.8], [38, -98], [39, -111], [39.3, -116.6]]

        for i, node in enumerate(nodes):
            # state = random.choice(state_coords)
            # state_coords.remove(state)
            state = state_coords[i]
            ni = NodeInfo()
            lat = fake.geo_coordinate(state[0], 0.5)
            long = fake.geo_coordinate(state[1], 0.5)
            ni.lat = lat
            ni.long = long
            ni.timestamp = int(time.time())

            db.session.add(ni)
            node.node_info.append(ni)
            db.session.commit()
