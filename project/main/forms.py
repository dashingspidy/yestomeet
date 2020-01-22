from flask_wtf import FlaskForm
from wtforms import (
    StringField, IntegerField,
    SelectField, TextAreaField)
from wtforms.validators import DataRequired, Email, Length
from flask_babel import gettext


class SearchForm(FlaskForm):
    age_min = SelectField(
        gettext('min'),
        coerce=int,
        choices=[(i, f"{i}") for i in range(18, 99)])
    age_max = SelectField(
        gettext('max'),
        coerce=int,
        choices=[(i, f"{i}") for i in range(18, 99)])
    gender = SelectField(
        gettext('sexe'),
        choices=[('men', gettext('un homme')), ('women', gettext('une femme'))])


class ContactForm(FlaskForm):
    nom = StringField(gettext('Votre nom'), validators=[DataRequired()])
    email = StringField(
        gettext('Votre email'), validators=[DataRequired()])
    telephone = StringField(gettext('Votre Téléphone'))
    message = TextAreaField(
        gettext('Votre message'), validators=[DataRequired(), Length(min=25)])
