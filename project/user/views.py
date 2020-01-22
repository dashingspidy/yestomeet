from flask import (
    Blueprint, render_template, redirect,
    url_for, flash)
from flask_login import (
    login_user, login_required, logout_user, current_user)
from flask_babel import gettext
from project import bcrypt
from .forms import (
    RegistrationForm, LoginForm, ForgotForm,
    ChangePasswordForm, UpdatePasswordForm)
from project.models import User, IntegrityError, database, Slider, DoesNotExist
from project.tokens import generate_confirmation_token, confirm_token
from project.mailer import (
    welcome_mail, confirmation_email, reset_email)
from project.helpers import age

user_blueprint = Blueprint('user', __name__)


@user_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        try:
            with database.transaction():
                user = User.create(
                    username=form.username.data,
                    email=form.email.data,
                    password_digest=bcrypt.generate_password_hash(form.password.data).decode('utf8'),
                    birthdate=form.birthdate.data,
                    location=form.location.data,
                    gender=form.gender.data,
                    looking_for=form.looking_for.data,
                    age=age(form.birthdate.data)
                )
                token = generate_confirmation_token(user.email)
                confirm_url = url_for(
                    'user.confirm_email', token=token, _external=True)
                welcome_mail(user.email, user.username)
                confirmation_email(
                    user.email,
                    user.username, confirm_url, user.email)
                login_user(user)
                return redirect(url_for('profile.new_profile'))
        except IntegrityError:
            raise ValueError(gettext('L\'utilisateur existe déjà'))
    return render_template('user/register.html', form=form)


@user_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        try:
            user = User.select().where(User.email == form.email.data).get()
        except User.DoesNotExist:
            flash(gettext('incorrecte Adresse email ou Mot de passe.'))
        else:
            if user and bcrypt.check_password_hash(user.password_digest, form.password.data):
                login_user(user)
                if user.profile:
                    return redirect(url_for('main.index'))
                else:
                    return redirect(url_for('profile.new_profile'))
            else:
                flash(gettext('incorrecte Adresse email ou Mot de passe.'))
    return render_template('user/login.html', form=form)


@user_blueprint.route('/forgot', methods=['GET', 'POST'])
def forgot():
    form = ForgotForm()
    if form.validate_on_submit():
        user = User.select().where(User.email == form.email.data).get()
        token = generate_confirmation_token(user.email)

        user.reset_digest = token
        user.save()

        reset_url = url_for('user.new_password', token=token, _external=True)
        reset_email(user.email, user.username, reset_url)
        flash(gettext('Un e-mail de réinitialisation de mot de passe a été envoyé.'))
        return redirect(url_for('main.index'))
    return render_template('user/forgot.html', form=form)


@user_blueprint.route('/new_password/<token>', methods=['GET', 'POST'])
def new_password(token):
    email = confirm_token(token)
    user = User.select().where(User.email == email).get()

    if user.reset_digest is not None:
        form = ChangePasswordForm()
        if form.validate_on_submit():
            user = User.select().where(User.email == email).get()
            if user:
                user.password_digest = bcrypt.generate_password_hash(form.password.data)
                user.reset_digest = None
                user.save()

                login_user(user)
                flash(gettext('votre mot de passe a été changé'))
                return redirect(url_for('profile.profile'))
            else:
                flash(gettext('Le changement de mot de passe a échoué'))
                return redirect(url_for('profile.profile'))
        else:
            return render_template('user/change_password.html', form=form)
    else:
        flash(gettext('Impossible de réinitialiser votre mot de passe'))
    return redirect(url_for('main.index'))


@user_blueprint.route('/update_password', methods=['GET', 'POST'])
@login_required
def update_password():
    user = User.get(User.id == current_user.id)
    form = UpdatePasswordForm()
    if form.validate_on_submit():
        user.password_digest = bcrypt.generate_password_hash(form.password.data)
        user.save()
        flash(gettext('votre mot de passe a été changé'))
        logout_user()
    return render_template('user/update_password.html', form=form)


@user_blueprint.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@user_blueprint.route('/confirm/<token>')
@login_required
def confirm_email(token):
    try:
        email = confirm_token(token)
    except:
        flash(gettext('Le lien de confirmation est invalide ou a expiré.'))
    user = User.select().where(User.email == email).get()
    if user.confirmed:
        flash(gettext('Votre compte déjà confirmé.'))
    else:
        user.confirmed = True
        user.save()
    return redirect(url_for('main.index'))


@user_blueprint.route('/resend')
@login_required
def resend_confirmation():
    token = generate_confirmation_token(current_user.email)
    confirm_url = url_for('user.confirm_email', token=token, _external=True)
    confirmation_email(
        current_user.email, current_user.username, confirm_url)
    flash(gettext('Un nouvel e-mail de confirmation a été envoyé'))
    return redirect(url_for('profile.profile'))


@user_blueprint.route('/subscribe')
def subscribe():
    user = current_user.get()
    if user.notif == 0:
        user.notif = True
        user.save()
    return redirect(url_for('main.my_account'))


@user_blueprint.route('/unsbscribe')
def unsbscribe():
    user = current_user.get()
    if user.notif == 1:
        user.notif = False
        user.save()
    return redirect(url_for('main.my_account'))
