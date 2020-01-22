from flask import render_template
from flask_mail import Message
from flask_babel import gettext

from project import app, mail


def send_mail(to, subject, template):
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=app.config['MAIL_DEFAULT_SENDER']
    )
    mail.send(msg)


def welcome_mail(to, username):
    template = render_template('email/welcome.html', username=username)
    msg = Message(
        subject=gettext('Bienvenue sur Yes To Meet You'),
        recipients=[to],
        html=template,
        sender=app.config['MAIL_DEFAULT_SENDER']
    )
    mail.send(msg)


def confirmation_email(to, username, confirm_url, email):
    template = render_template(
        'user/activate.html',
        username=username, confirm_url=confirm_url, email=email)
    msg = Message(
        subject=gettext('Confirmation'),
        recipients=[to],
        html=template,
        sender=app.config['MAIL_DEFAULT_SENDER']
    )
    mail.send(msg)


def reset_email(to, username, reset_url):
    template = render_template(
        'user/reset.html', username=username, reset_url=reset_url)
    msg = Message(
        subject=gettext('Votre mot de passe'),
        recipients=[to],
        html=template,
        sender=app.config['MAIL_DEFAULT_SENDER']
    )
    mail.send(msg)


def visit_notif(to, current_user, username, slogan):
    template = render_template(
        'email/visit-notification.html',
        current_user=current_user, username=username,
        slogan=slogan)
    msg = Message(
        subject=gettext('{} a visité votre profil'.format(current_user)),
        recipients=[to],
        html=template,
        sender=app.config['MAIL_DEFAULT_SENDER'])
    mail.send(msg)


def message_notif(to, current_user, username, message):
    template = render_template(
        'email/message-notification.html',
        current_user=current_user,
        username=username, message=message)
    msg = Message(
        subject=gettext('Un nouveau message de {}'.format(current_user)),
        recipients=[to],
        html=template,
        sender=app.config['MAIL_DEFAULT_SENDER'])
    mail.send(msg)
