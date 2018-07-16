
from flask import render_template, Blueprint, jsonify


home = Blueprint('home', __name__, '/', template_folder='../templates')


@home.route('/')
@home.route('/index')
def index():
    return render_template('index.html', title='Home | Flask-Startup')


@home.route('/contact')
def contact():
    return render_template('contact.html', title='Contact | Flask-Startup')


@home.route('/faq')
def faq():
    return render_template('faq.html', title='FAQ | Flask-Startup')


@home.route('/map')
def map():
    return render_template('realtime_map.html', title='Device Map | Flask-Startup')


@home.route('/test')
def test():
    return jsonify()