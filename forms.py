from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from models import User


class RegistrationForm(FlaskForm):
    """
    Форма регистрации пользователя.
    
    Поля:
        username: Имя пользователя (3-80 символов)
        email: Email (валидный формат)
        password: Пароль (минимум 6 символов)
        password2: Подтверждение пароля (должен совпадать)
    """
    username = StringField(
        'Имя пользователя',
        validators=[
            DataRequired(message='Введите имя пользователя'),
            Length(min=3, max=80, message='Имя должно быть от 3 до 80 символов')
        ]
    )
    email = StringField(
        'Email',
        validators=[
            DataRequired(message='Введите email'),
            Email(message='Введите корректный email')
        ]
    )
    password = PasswordField(
        'Пароль',
        validators=[
            DataRequired(message='Введите пароль'),
            Length(min=6, message='Пароль должен быть не менее 6 символов')
        ]
    )
    password2 = PasswordField(
        'Подтверждение пароля',
        validators=[
            DataRequired(message='Подтвердите пароль'),
            EqualTo('password', message='Пароли должны совпадать')
        ]
    )
    submit = SubmitField('Зарегистрироваться')
    
    def validate_username(self, username):
        """Проверка: имя пользователя должно быть уникальным."""
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Это имя уже занято. Выберите другое.')
    
    def validate_email(self, email):
        """Проверка: email должен быть уникальным."""
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Этот email уже зарегистрирован.')


class LoginForm(FlaskForm):
    """
    Форма входа пользователя.
    
    Поля:
        email: Email пользователя
        password: Пароль
        remember_me: Запомнить меня
    """
    email = StringField(
        'Email',
        validators=[
            DataRequired(message='Введите email'),
            Email(message='Введите корректный email')
        ]
    )
    password = PasswordField(
        'Пароль',
        validators=[
            DataRequired(message='Введите пароль')
        ]
    )
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')
