from flask import Blueprint, render_template, redirect, url_for, abort, flash, jsonify, abort, request
import json
import sys

from app import models
from app.core import db
from app.schemas import data
from app.toolbox import validate

api = Blueprint('api', __name__, '/api')


@api.route('/api/add_data', methods=['POST'])
# @validate.validate_schema(data.new_data)
def add_data():
    print(request, file=sys.stderr)
    posted = request.get_json()
    print(posted, file=sys.stderr)
    data = dict(
        lat=posted['lat'],
        long=posted['long']
    )
    save_data(data)
    return jsonify(dict(msg='data saved!'))


@api.route('/api/get_data', methods=['GET'])
def get_data():
    data = retrieve_data()
    return jsonify(dict(msg=data))


def retrieve_data():
    try:
        with open('data.json', 'r') as infile:
            data = json.load(infile)
    except FileNotFoundError:
        return []
    return data


def save_data(new_data):
    data = retrieve_data()
    with open('data.json', 'w') as outfile:
        data.append(new_data)
        json.dump(data, outfile, sort_keys=True, indent=4)
