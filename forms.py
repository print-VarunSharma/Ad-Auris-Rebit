from flask_wtf import FlaskForm
from wtforms import StringField, TextField, SubmitField

from wtforms.validators import DataRequired, Length
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import (StringField,
                     TextAreaField,
                     SubmitField,
                     PasswordField,
                     DateField,
                     SelectField)
from wtforms.validators import (DataRequired,
                                Email,
                                EqualTo,
                                Length,
                                URL)

class FeedbackForm(FlaskForm):
    """Contact Form."""
    email = StringField('Email', [
        Email(message='Not a valid email address.'),
        DataRequired()])
    password = PasswordField('Password', [
        DataRequired(message="Please enter a password."),
    ])
    confirmPassword = PasswordField('Repeat Password', [
            EqualTo(password, message='Passwords must match.')
            ])
    title = SelectField('Title', [DataRequired()],
                        choices=[("I'm a current customer with Ad-Auris"),
                                 ('User'),
                                 ("Newsletter"),
                                 ('Publisher'),
                                 ('Blogger'),
                                 ('Other')])
    website = StringField('Website', validators=[URL()])
    recaptcha = RecaptchaField()
    submit = SubmitField('Submit')

class ContactForm(FlaskForm):
    """Contact form."""
    name = StringField('Name', [
        DataRequired()])
    email = StringField('Email', [
        Email(message=('Not a valid email address.')),
        DataRequired()])
    body = TextField('Message', [
        DataRequired(),
        Length(min=4, message=('Your message is too short.'))])
    recaptcha = RecaptchaField()
    submit = SubmitField('Submit')