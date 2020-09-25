"""Database models."""
from . import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class Wallet(db.Model):
    __tablename__ = 'wallet'
    wallet_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False, unique=False)
    balance = db.Column(db.Float, nullable=False, unique=False, server_default="0.0")
    lock_operation = db.Column(db.Integer, nullable=False, unique=False, server_default="0")

class Operation(db.Model):
    __tablename__ = 'operation'
    operation_id = db.Column(db.Integer, primary_key=True)
    wallet_id = db.Column(db.Integer, nullable=False, unique=False, index=True)
    amount = db.Column(db.Float, nullable=False, unique=False)
    details = db.Column(db.String(100), nullable=False, unique=False)
    timestamp = db.Column(db.DateTime, nullable=False, unique=False)
    debet = db.Column(db.Boolean, nullable=False, unique=False)  # True - Дебет,списание с кошелька, False - Кредит, зачисление на кошелек
    opertype = db.Column(db.String(20), nullable=False, unique=False)  # external_in (зачисление на кошелек), w2w_onestep (перевод с кошелька на кошелек в один шаг)
    contragent_id = db.Column(db.Integer, nullable=False, unique=False, index=True) # 0 - not wallet, >0 - another wallet

class User(UserMixin, db.Model):
    """User account model."""

    __tablename__ = 'flasklogin-users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=False)
    email = db.Column(db.String(40), unique=True, nullable=False)
    password = db.Column(db.String(200), primary_key=False, unique=False, nullable=False)
    created_on = db.Column(db.DateTime, index=False, unique=False, nullable=True)
    last_login = db.Column(db.DateTime, index=False, unique=False, nullable=True)

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password, method='sha256')

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)
