from flask_wtf import FlaskForm
from wtforms import TextAreaField
from wtforms.validators import DataRequired, Length
from flask_babel import gettext


class ReportForm(FlaskForm):
    message = TextAreaField(
        gettext('Votre message'),
        validators=[DataRequired(), Length(min=50)])
