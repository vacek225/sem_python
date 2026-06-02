from __future__ import annotations

from flask_wtf import FlaskForm
from wtforms import FloatField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange


class RegisterForm(FlaskForm):
    username = StringField("Имя пользователя", validators=[DataRequired(), Length(min=3, max=80)])
    password = PasswordField("Пароль", validators=[DataRequired(), Length(min=6, max=128)])
    submit = SubmitField("Создать аккаунт")


class LoginForm(FlaskForm):
    username = StringField("Имя пользователя", validators=[DataRequired(), Length(min=3, max=80)])
    password = PasswordField("Пароль", validators=[DataRequired()])
    submit = SubmitField("Войти")


class PredictionForm(FlaskForm):
    sepal_length = FloatField(
        "Длина чашелистика",
        validators=[DataRequired(), NumberRange(min=0.1, max=20)],
    )
    sepal_width = FloatField(
        "Ширина чашелистика",
        validators=[DataRequired(), NumberRange(min=0.1, max=20)],
    )
    petal_length = FloatField(
        "Длина лепестка",
        validators=[DataRequired(), NumberRange(min=0.1, max=20)],
    )
    petal_width = FloatField(
        "Ширина лепестка",
        validators=[DataRequired(), NumberRange(min=0.1, max=20)],
    )
    submit = SubmitField("Получить предсказание")
