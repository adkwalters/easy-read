from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email


class ContactForm(FlaskForm):
    """A form to collect and validate an email message"""
    name                = StringField('Name', validators=[DataRequired()])
    email               = StringField('Email', validators=[DataRequired(), Email()])
    subject             = StringField('Subject', validators=[DataRequired()])
    message             = TextAreaField('Message', validators=[DataRequired()])
    submit              = SubmitField('Send')

