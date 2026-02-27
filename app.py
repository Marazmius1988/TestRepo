import os
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, User
from forms import RegistrationForm, LoginForm

# Инициализация приложения
app = Flask(__name__)

# Конфигурация
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Инициализация расширений (используем db из models.py)
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Пожалуйста, войдите для доступа к этой странице'
login_manager.login_message_category = 'warning'


# Загрузка пользователя для Flask-Login
@login_manager.user_loader
def load_user(user_id):
    """Загружает пользователя по ID для сессии."""
    return User.query.get(int(user_id))


# Маршруты
@app.route('/')
def index():
    """Главная страница."""
    return render_template('index.html')


@app.route('/about')
def about():
    """Страница 'О нас'."""
    return render_template('about.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    """Страница регистрации."""
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        # Создаём нового пользователя
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)

        # Сохраняем в БД
        db.session.add(user)
        db.session.commit()

        flash('Регистрация успешна! Теперь вы можете войти.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Страница входа."""
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        # Ищем пользователя по email
        user = User.query.filter_by(email=form.email.data).first()

        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            flash('Вы успешно вошли!', 'success')

            # Перенаправляем на страницу, куда пытались зайти, или на главную
            next_page = request.args.get('next')
            return redirect(next_page or url_for('index'))

        flash('Неверный email или пароль', 'error')

    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    """Выход из системы."""
    logout_user()
    flash('Вы вышли из системы', 'info')
    return redirect(url_for('index'))


@app.route('/profile')
@login_required
def profile():
    """Личный кабинет пользователя."""
    return render_template('profile.html', user=current_user)


# Создание БД при первом запуске
def create_database():
    """Создаёт базу данных и таблицы."""
    with app.app_context():
        db.create_all()
        print('База данных создана!')


if __name__ == '__main__':
    create_database()
    app.run(debug=True)
