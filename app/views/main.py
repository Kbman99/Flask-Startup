from flask import render_template
from app import app, db, models
import sys


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')


@app.route('/contact')
def contact():
    return render_template('contact.html', title='Contact')


@app.route('/faq')
def faq():
    return render_template('faq.html', title='FAQ')


@app.route('/map')
def map():
    return render_template('realtime_map.html', title='Its a Map')
