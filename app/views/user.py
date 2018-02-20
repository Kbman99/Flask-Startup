from flask import Blueprint, render_template, redirect, url_for, abort, flash, current_app, request
from flask_login import login_user, logout_user, login_required

from app.core import db
from app import models
from app.forms import user as user_forms
from app.toolbox import email
from flask import current_app


import time
import sys

import app

from itsdangerous import URLSafeTimedSerializer

# Create a user blueprint
user = Blueprint('user', __name__, url_prefix='/user')


@user.record
def setup(state):
    ts = URLSafeTimedSerializer(state.app.config['SECRET_KEY'])


@user.route('/signup', methods=['GET', 'POST'])
def signup():
    form = user_forms.SignUp()
    if form.validate_on_submit():
        user = models.User(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            confirmation=0,
            password=form.password.data
        )
        db.session.add(user)
        db.session.commit()
        subject = 'Please confirm your email address.'
        token = URLSafeTimedSerializer(current_app.config['SECRET_KEY']).dumps(user.email, salt='email-confirm-key')
        confirmUrl = url_for('user.confirm', token=token, _external=True)
        html = render_template('email/confirm.html',
                               confirm_url=confirmUrl)
        email.send(user.email, subject, html)
        flash('Check your emails to confirm your email address.', 'positive')
        return redirect(url_for('home.index'))
    return render_template('user/signup.html', form=form, title='Sign up')


@user.route('/confirm/<token>', methods=['GET', 'POST'])
def confirm(token):
    try:
        email = URLSafeTimedSerializer(current_app.config['SECRET_KEY']).loads(token, salt='email-confirm-key', max_age=86400)
    except:
        abort(404)

    user = models.User.query.filter_by(email=email).first()
    user.confirmation = True
    db.session.commit()
    flash(
        'Your email address has been confirmed, you can sign in.', 'positive')
    return redirect(url_for('user.signin'))


@user.route('/signin', methods=['GET', 'POST'])
def signin():
    form = user_forms.Login()
    if form.validate_on_submit():
        user = models.User.query.filter_by(email=form.email.data).first()
        if user is not None:
            if user.check_password(form.password.data):
                login_user(user)
                flash('Succesfully signed in.', 'positive')
                return redirect(url_for('home.index'))
            else:
                flash('The password you have entered is wrong.', 'negative')
                return redirect(url_for('user.signin'))
        else:
            flash('Unknown email address.', 'negative')
            return redirect(url_for('user.signin'))
    return render_template('user/signin.html', form=form, title='Sign in')


@user.route('/signout')
def signout():
    logout_user()
    flash('Succesfully signed out.', 'positive')
    return redirect(url_for('home.index'))


@user.route('/resend', methods=['GET', 'POST'])
def resend():
    form = user_forms.Resend()
    if form.validate_on_submit():
        user = models.User.query.filter_by(email=form.email.data).first()
        if user is not None:
            subject = 'Please confirm your email address.'
            token = URLSafeTimedSerializer(current_app.config['SECRET_KEY']).dumps(user.email, salt='email-confirm-key')
            confirmUrl = url_for('user.confirm', token=token, _external=True)
            html = render_template('email/confirm.html',
                                   confirm_url=confirmUrl)
            email.send(user.email, subject, html)
            flash('Your confirmation email has been successfully resent. '
                  'Check your emails to confirm your email address.', 'positive')
            return redirect(url_for('home.index'))
        else:
            flash('Unknown email address.', 'negative')
            return redirect(url_for('home.index'))
    return render_template('user/resend.html', form=form)


@user.route('/account')
@login_required
def account():
    return render_template('user/account.html', title='Account')


@user.route('/forgot', methods=['GET', 'POST'])
def forgot():
    form = user_forms.Forgot()
    if form.validate_on_submit():
        user = models.User.query.filter_by(email=form.email.data).first()
        if user is not None:
            subject = 'Reset your password.'
            token = URLSafeTimedSerializer(current_app.config['SECRET_KEY']).dumps(user.email, salt='password-reset-key')
            resetUrl = url_for('user.reset', token=token, _external=True)
            html = render_template('email/reset.html', reset_url=resetUrl)
            email.send(user.email, subject, html)
            flash('Check your emails to reset your password.', 'positive')
            return redirect(url_for('home.index'))
        else:
            flash('Unknown email address.', 'negative')
            return redirect(url_for('user.forgot'))
    return render_template('user/forgot.html', form=form)


@user.route('/reset/<token>', methods=['GET', 'POST'])
def reset(token):
    try:
        email = URLSafeTimedSerializer(current_app.config['SECRET_KEY']).loads(token, salt='password-reset-key', max_age=86400)
    except Exception:
        abort(404)
    form = user_forms.Reset()
    if form.validate_on_submit():
        user = models.User.query.filter_by(email=email).first()
        if user is not None:
            user.password = form.password.data
            db.session.commit()
            flash('Your password has been reset, you can sign in.', 'positive')
            return redirect(url_for('user.signin'))
        else:
            flash('Unknown email address.', 'negative')
            return redirect(url_for('user.forgot'))
    return render_template('user/reset.html', form=form, token=token)


@user.route('/deviceManager', methods=['GET', 'POST'])
@login_required
def device_manager():
    g_form = user_forms.Gateway()
    n_form = user_forms.Node()
    return render_template('user/devices.html', g_form=g_form, n_form=n_form)
    #return render_template('user/devices.html', n_form=n_form)


@user.route('/deviceInfo', methods=['GET', 'POST'])
@login_required
def device_info():
    if request.method == 'GET':
        return render_template('user/device_info.html', title='Device Information')
    elif request.method == 'POST':
        node_id = request.values.get('node')
        node = models.Node.query.filter(models.Node.node_id == node_id).first()
        return render_template('user/device_info.html', data=node.node_info[::-1], node_id=node_id)
