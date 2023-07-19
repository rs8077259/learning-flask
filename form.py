
from flask_wtf import FlaskForm
import wtforms as form
from wtforms.validators import *


class FeedBack(FlaskForm):
    email=form.EmailField("Email:",validators=[DataRequired()])
    errorCode=form.StringField("error id:",validators=[DataRequired()])
    feedBack=form.TextAreaField("Your Valuable FeedBack:",validators=[DataRequired("feedback can't be empty")])
    submit=form.SubmitField("send Feedback")

class SignUp(FlaskForm):
    email=form.EmailField("Email",validators=[DataRequired("email is must to create your account")])
    password=form.PasswordField("Password",validators=[DataRequired()])
    submit=form.SubmitField("Sign up")



