from flask_sqlalchemy import SQLAlchemy # type: ignore
from flask_bcrypt import Bcrypt # type: ignore
from datetime import datetime
import uuid

db = SQLAlchemy()
bcrypt = Bcrypt()

class User(db.Model):
    """Modelo de usuario para la base de datos"""
    __tablename__ = 'users'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(128), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    email_verified = db.Column(db.Boolean, default=False, nullable=False)
    newsletter_subscription = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    last_login = db.Column(db.DateTime)
    
    # Campos adicionales para perfil de vino
    preferred_price_min = db.Column(db.Float, default=10.0)
    preferred_price_max = db.Column(db.Float, default=50.0)
    preferred_rating_min = db.Column(db.Float, default=4.0)
    favorite_regions = db.Column(db.Text)  # JSON string de regiones favoritas
    wine_experience_level = db.Column(db.String(20), default='beginner')  # beginner, intermediate, expert
    
    def __init__(self, email, password, first_name, last_name, birth_date, newsletter_subscription=False):
        self.email = email.lower().strip()
        self.first_name = first_name.strip()
        self.last_name = last_name.strip()
        self.birth_date = birth_date
        self.newsletter_subscription = newsletter_subscription
        self.set_password(password)
    
    def set_password(self, password):
        """Hashea y guarda la contraseña"""
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    
    def check_password(self, password):
        """Verifica la contraseña"""
        return bcrypt.check_password_hash(self.password_hash, password)
    
    def get_full_name(self):
        """Retorna el nombre completo"""
        return f"{self.first_name} {self.last_name}"
    
    def get_age(self):
        """Calcula la edad actual"""
        today = datetime.now().date()
        age = today.year - self.birth_date.year
        if today.month < self.birth_date.month or (today.month == self.birth_date.month and today.day < self.birth_date.day):
            age -= 1
        return age
    
    def is_adult(self):
        """Verifica si es mayor de edad"""
        return self.get_age() >= 18
    
    def to_dict(self):
        """Convierte el usuario a diccionario para JSON"""
        return {
            'id': self.id,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'full_name': self.get_full_name(),
            'age': self.get_age(),
            'is_active': self.is_active,
            'email_verified': self.email_verified,
            'newsletter_subscription': self.newsletter_subscription,
            'created_at': self.created_at.isoformat(),
            'wine_experience_level': self.wine_experience_level,
            'preferred_price_range': f"{self.preferred_price_min}-{self.preferred_price_max}€"
        }
    
    def __repr__(self):
        return f'<User {self.email}>'

class UserSession(db.Model):
    """Modelo para sesiones de usuario"""
    __tablename__ = 'user_sessions'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    session_token = db.Column(db.String(128), unique=True, nullable=False)
    ip_address = db.Column(db.String(45))  # IPv6 compatible
    user_agent = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    
    # Relación con User
    user = db.relationship('User', backref=db.backref('sessions', lazy=True))
    
    def __repr__(self):
        return f'<UserSession {self.user_id}>'

class WineRecommendation(db.Model):
    """Modelo para guardar recomendaciones de vinos de usuarios"""
    __tablename__ = 'wine_recommendations'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    
    # Parámetros de búsqueda
    precio_min = db.Column(db.Float, nullable=False)
    precio_max = db.Column(db.Float, nullable=False)
    rating_min = db.Column(db.Float, nullable=False)
    ocasion = db.Column(db.String(50))
    gusto = db.Column(db.String(50))
    
    # Resultado de la predicción
    prediccion = db.Column(db.String(50))
    confianza = db.Column(db.Float)
    
    # Vinos recomendados (JSON)
    vinos_recomendados = db.Column(db.Text)  # JSON string
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Relación con User
    user = db.relationship('User', backref=db.backref('recommendations', lazy=True))
    
    def __repr__(self):
        return f'<WineRecommendation {self.user_id} - {self.prediccion}>'
