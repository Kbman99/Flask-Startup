from flask import render_template, Blueprint

import app

home = Blueprint('home', __name__, '/', template_folder='../templates')


@home.route('/')
@home.route('/index')
def index():
    return render_template('index.html', title='Home')


@home.route('/contact')
def contact():
    return render_template('contact.html', title='Contact')


@home.route('/faq')
def faq():
    return render_template('faq.html', title='FAQ')


@home.route('/map')
def map():
    return render_template('realtime_map.html', title='Its a Map')


# @app.route('/')
# @app.route('/index')
# def index():
#     return render_template('index.html', title='Home')
#
#
# @app.route('/contact')
# def contact():
#     return render_template('contact.html', title='Contact')
#
#
# @app.route('/faq')
# def faq():
#     return render_template('faq.html', title='FAQ')
#
#
# @app.route('/map')
# def map():
#     return render_template('realtime_map.html', title='Its a Map')
