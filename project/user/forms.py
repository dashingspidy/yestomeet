from flask_wtf import FlaskForm
from wtforms import (
    StringField, PasswordField, SubmitField,
    DateField, SelectField, BooleanField)
from wtforms.validators import (
    DataRequired, EqualTo, Email,
    ValidationError, Length)
from flask_babel import gettext

from project.models import User
from project import current_user, bcrypt


def email_exist(form, field):
    if User.select().where(User.email == field.data).exists():
        raise ValidationError('Vous êtes déjà inscrit')


def username_exist(form, field):
    if User.select().where(User.username == field.data).exists():
        raise ValidationError('Pseudo déjà pris')


def email_not_exist(form, field):
    if not User.select().where(User.email == field.data):
        raise ValidationError('Adresse Email n\'existe pas')


def password_does_not_match(form, field):
    if not bcrypt.check_password_hash(current_user.password_digest, field.data):
        raise ValidationError(gettext('mot de passe incorrect'))


class RegistrationForm(FlaskForm):
    birthdate = DateField(
        gettext('Date de naissance'),
        format='%m/%d/%Y',
        validators=[DataRequired()],
        render_kw={"placeholder": gettext('Date de naissance')})
    gender = SelectField(
        gettext('Je suis'),
        choices=[('men', gettext('un homme')), ('women', gettext('une femme'))],
        validators=[DataRequired()])
    looking_for = SelectField(
        gettext('cherchant'),
        choices=[('women', gettext('une femme')), ('men', gettext('un homme'))],
        validators=[DataRequired()])
    location = StringField(gettext('Ville'), validators=[DataRequired()])
    username = StringField(
        gettext('Pseudo'),
        validators=[DataRequired(), Length(min=6), username_exist],
        render_kw={"placeholder": gettext('Pseudo')})
    email = StringField(
        gettext('Adresse Email'),
        validators=[DataRequired(), Email(), email_exist],
        render_kw={"placeholder": gettext('Adresse Email')})
    password = PasswordField(
        gettext('Mot de passe'),
        validators=[
            DataRequired(),
            EqualTo('confirm', message="Password must match"),
            Length(min=6)
        ],
        render_kw={"placeholder": gettext('6 caractères alphanumériques minimum')})
    confirm = PasswordField(gettext('Confirmation de mot de passe'))
    checkbox = BooleanField(
        gettext('Agree'), default=False, validators=[DataRequired()])
    submit = SubmitField(gettext("Continuer l'inscription"))


class LoginForm(FlaskForm):
    email = StringField(
        gettext('Adresse Email'), validators=[DataRequired(), Email()])
    password = PasswordField(
        gettext('Mot de passe'), validators=[DataRequired()])
    submit = SubmitField(gettext('Se connecter'))


class ForgotForm(FlaskForm):
    email = StringField(
        gettext('Adresse Email'),
        validators=[
            DataRequired(), Email(), email_not_exist
        ])


class ChangePasswordForm(FlaskForm):
    password = PasswordField(
        gettext('Mot de passe'), validators=[DataRequired(), Length(min=6)])
    confirm = PasswordField(
        gettext('Confirmation de mot de passe'),
        validators=[
            DataRequired(),
            EqualTo('password', message='Password must match')
        ])


class UpdatePasswordForm(FlaskForm):
    current_password = PasswordField(
        gettext('Mot de passe actuel'),
        validators=[DataRequired(), password_does_not_match])
    password = PasswordField(
        gettext('Mot de passe'), validators=[DataRequired(), Length(min=6)])
    confirm = PasswordField(
        gettext('Confirmation de mot de passe'),
        validators=[
            DataRequired(),
            EqualTo('password', message='Password must match')
        ])
