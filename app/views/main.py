from flask import render_template, Blueprint, jsonify


home = Blueprint('home', __name__, '/', template_folder='../templates')


@home.route('/')
@home.route('/index')
def index():
    return render_template('index_iot.html', title='Home')


@home.route('/contact')
def contact():
    return render_template('contact.html', title='Contact')


@home.route('/faq')
def faq():
    return render_template('faq.html', title='FAQ')


@home.route('/map')
def map():
    return render_template('realtime_map.html', title='Device Map')


@home.route('/test')
def test():

    return jsonify()
