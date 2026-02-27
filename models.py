from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# Создаём экземпляр db здесь, чтобы использовать во всём проекте
db = SQLAlchemy()


class User(UserMixin, db.Model):
    """
    Модель пользователя.
    
    Атрибуты:
        id: Уникальный идентификатор (автоинкремент)
        username: Имя пользователя (уникальное, обязательное)
        email: Email (уникальный, обязательный)
        password_hash: Хэш пароля (не храним пароль в открытом виде!)
        created_at: Дата регистрации
        is_active: Активен ли пользователь
    """
    __tablename__ = 'users'  # Имя таблицы в БД
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    def set_password(self, password):
        """
        Устанавливает хэш пароля.
        
        Args:
            password: Пароль в открытом виде
        """
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """
        Проверяет пароль.
        
        Args:
            password: Пароль для проверки
            
        Returns:
            bool: True если пароль верный
        """
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        """Строковое представление для отладки."""
        return f'<User {self.username}>'
