from wtforms import StringField, PasswordField, SubmitField, TextAreaField, BooleanField
from wtforms.fields import EmailField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm


class DecksForm(FlaskForm):  # Форма для редактирования/добавления колоды
    title = StringField('Название колоды', validators=[DataRequired()])
    commander1 = StringField('Командир (опционально)')
    commander2 = StringField('Второй командир (опционально)')
    content = TextAreaField("Деклист", validators=[DataRequired()])
    is_private = BooleanField("Личное")
    submit = SubmitField('Cохранить')


class RegisterForm(FlaskForm):  # Форма для регистрации
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    name = StringField('Имя пользователя', validators=[DataRequired()])
    submit = SubmitField('Войти')


class LoginForm(FlaskForm):  # Форма для входа
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')
