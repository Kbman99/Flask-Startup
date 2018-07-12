from threading import Thread
from flask_mail import Message
from ..core import mail
from ..config import base_config
from flask import current_app


def send(recipient, subject, body):
    """
    Send a mail to a recipient. The body is usually a rendered HTML template.
    The sender's credentials has been configured in the config.py file.
    """
    sender = base_config.ADMINS[0]
    message = Message(subject, sender=sender, recipients=[recipient])
    message.html = body
    # Create a new thread
    app = current_app._get_current_object()
    thr = Thread(target=send_async, args=[app, message])
    thr.start()


def send_async(app, message):
    """Send the mail asynchronously."""
    with app.app_context():
        mail.send(message)