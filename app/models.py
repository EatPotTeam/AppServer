import random, string
from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from . import db


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)
    orders = db.relationship('Order', backref='user')
    coupons = db.relationship('Coupon', backref='user')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    @staticmethod
    def confirm(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        user = User.query.get(int(data['confirm']))
        user.confirmed = True
        db.session.add(user)
        db.session.commit()
        return True

    def generate_auth_token(self, expiration):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None
        return User.query.get(int(data['id']))


ORDER_STATUS = {
    'WAITING': False,
    'PAID': True
}


class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    cinema_name = db.Column(db.UnicodeText)
    movie_name = db.Column(db.UnicodeText)
    broadcast_id = db.Column(db.Integer)
    time = db.Column(db.String(10))
    total_price = db.Column(db.Integer)
    status = db.Column(db.Boolean, default=ORDER_STATUS['WAITING'])
    redeem_code = db.Column(db.String(15), unique=True, nullable=True)
    order_items = db.relationship('OrderItem')
    coupons_used = db.relationship('Coupon')

    @staticmethod
    def generate_redeem_code():
        length = 12
        source = list(string.ascii_uppercase)
        for i in range(0, 10):
            source.append(str(i))
        code = ''
        for index in range(length):
            code += random.choice(source)
        return code


class OrderItem(db.Model):
    __tablename__ = 'orderitems'
    id = db.Column(db.Integer, primary_key=True)
    row = db.Column(db.Integer)
    col = db.Column(db.Integer)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))


class Coupon(db.Model):
    __tablename__ = 'coupons'
    id = db.Column(db.Integer, primary_key=True)
    discount_price = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=True)