from app.models import User, NodeInfo
from .core import scheduler, db
from faker import Faker
import time
import random
import sys

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

            if 0 < random.randrange(0, 100) < 10:
                ni.status = random.randrange(1, 4)
            else:
                ni.status = 0

            if ni.status == 3:
                node.status = 0
            elif ni.status != 0:
                node.status = ni.status

            #print('node {} has status {}'.format(node.node_id, node.status), sys.stderr)

            db.session.add(ni)
            node.node_info.append(ni)
            db.session.commit()

#
# nets = wlan.scan()
# for net in nets:
#     if net.ssid == 'Jeremiah':
#         print('Network found!')
#         wlan.connect(net.ssid, auth=(net.sec, '7546664988'), timeout=5000)
#         while not wlan.isconnected():
#             machine.idle() # save power while waiting
#         print('WLAN connection succeeded!')
#         break