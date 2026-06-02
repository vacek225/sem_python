from __future__ import annotations

from flask_wtf import FlaskForm
from wtforms import FloatField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange


class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=3, max=80)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6, max=128)])
    submit = SubmitField("Create account")


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=3, max=80)])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Sign in")


class PredictionForm(FlaskForm):
    sepal_length = FloatField(
        "Sepal length",
        validators=[DataRequired(), NumberRange(min=0.1, max=20)],
    )
    sepal_width = FloatField(
        "Sepal width",
        validators=[DataRequired(), NumberRange(min=0.1, max=20)],
    )
    petal_length = FloatField(
        "Petal length",
        validators=[DataRequired(), NumberRange(min=0.1, max=20)],
    )
    petal_width = FloatField(
        "Petal width",
        validators=[DataRequired(), NumberRange(min=0.1, max=20)],
    )
    submit = SubmitField("Predict")
