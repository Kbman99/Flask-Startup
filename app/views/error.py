from flask import render_template, Blueprint

error = Blueprint('error', __name__, template_folder='../templates')


@error.errorhandler(403)
def forbidden(e):
    return render_template('error.html', message='403 forbidden'), 403


@error.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', message='404 not found'), 404


@error.errorhandler(410)
def gone(e):
    return render_template('error.html', message='410 gone'), 410


@error.errorhandler(500)
def internal_error(e):
    return render_template('error.html', message='500 internal error'), 500
