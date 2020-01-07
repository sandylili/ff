from flask_wtf  import  Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User


class LoginForm(Form):
    username = StringField('username', validators=[Required()])
    password = StringField('Password', validators=[Required()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')


class changepasswordForm(Form):
    username = StringField('username', validators=[Required()])
    
    oldpassword = StringField('oldPassword', validators=[Required()])
    newpassword = StringField('newPassword', validators=[Required()])
    submit = SubmitField('change')


