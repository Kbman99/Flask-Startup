from flask import Blueprint, render_template, redirect, url_for, abort, flash, jsonify, abort, request
import json
import sys

from app.models import User, Gateway, Node, NodeInfo
from app.core import db
from app.forms import user as user_forms
from app.schemas import data
from app.toolbox import validate

from flask_login import current_user

api = Blueprint('api', __name__, '/api')


@api.route('/add/device/<device_type>', methods=['POST'])
def add_device(device_type):
    if device_type == 'gateway':
        g_form = user_forms.Gateway()
        if g_form.validate_on_submit():
            g = Gateway(
                gateway_id=g_form.gateway_id.data
            )
            db.session.add(g)
            u = User.query.filter(User.id == current_user.id).first()
            u.gateways.append(g)
            db.session.commit()
            flash("Gateway {} has been successfully added!".format(g.gateway_id), 'positive')
    elif device_type == 'node':
        n_form = user_forms.Node()
        if n_form.validate_on_submit():
            u = User.query.filter(User.id == current_user.id).first()
            g = Gateway.query.filter(Gateway.user == current_user.id)\
                .filter(Gateway.gateway_id == n_form.parent_gateway.data).first()
            if g:
                n = Node(
                    node_id=n_form.node_id.data
                )
                db.session.add(n)
                g.child_nodes.append(n)
                db.session.commit()
                flash("Gateway {} has been successfully added!"
                      .format(n.node_id, n_form.parent_gateway.data), 'positive')
            else:
                flash("The node {} was not created. The gateway {} does not exist!"
                      .format(n_form.node_id.data, n_form.parent_gateway.data), 'negative')
    return redirect(url_for('user.device_manager'))


@api.route('/api/remove_device', methods=['POST'])
def remove_device():
    posted = request.get_json(force=True)
    if posted['device'] == 'gateway':
        g = Gateway.query.filter(Gateway.gateway_id == posted['id']).first()

        db.session.delete(g)
        db.session.commit()
    elif posted['device'] == 'node':
        n = Node.query.filter(Node.node_id == posted['id']).first()

        db.session.delete(n)
        db.session.commit()
    return jsonify(dict(msg='data saved!'))


@api.route('/api/add_data', methods=['POST'])
# @validate.validate_schema(data.new_data)
def add_data():
    posted = request.get_json()

    return jsonify(dict(msg='data saved!'))


@api.route('/api/get_data/<id>', methods=['GET'])
def get_data(id):
    items = retrieve_data(id)
    geo_items = generate_geojson(items)
    return jsonify(dict(geo_items))


def retrieve_data(id):
    try:
        user = User.query.filter(User.id == id).first()
        nodes = [n for g in user.gateways for n in g.child_nodes]
        data = {}
        for node in nodes:
            node_info = NodeInfo.query.join(Node).filter(Node.node_id == node.node_id).order_by(NodeInfo.id.desc()).first()
            if node_info:
                data[node.node_id] = {
                    'id': node.node_id,
                    'lat': node_info.lat,
                    'long': node_info.long
                }
        return data
    except Exception as e:
        print(e, sys.stderr)
        return {}


def generate_geojson(data):
    geo_json_schema = {
      "type": "FeatureCollection",
      "features": []
    }
    for k, v in data.items():
        geo_json_schema["features"].append({
            "type": "Feature",
            "properties": {
                "node_id": k,
                "Status": ""
            },
            "geometry": {
                "type": "Point",
                "coordinates": [
                    v["long"],
                    v["lat"]
                ]
            }
        })
    return geo_json_schema
