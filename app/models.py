from datetime import datetime
import hashlib
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from markdown import markdown
import bleach
from flask import current_app, request, url_for
from flask_login import UserMixin, AnonymousUserMixin

from . import db, login_manager


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')



    def __repr__(self):
        return '<Role %r>' % self.name


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password = db.Column(db.String(128))
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow)
    changgeruser= db.relationship('InOut', backref='user')

    def verify_password(self,inpassword):
        return inpassword == self.password


    def can(self, permissions):
        return self.role is not None and \
            (self.role.permissions & permissions) == permissions

    def is_administrator(self):
        return self.can(1)



    def __repr__(self):
        return '<User %r>' % self.username


class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False

login_manager.anonymous_user = AnonymousUser


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))




class Good(db.Model):
    __tablename__ = 'goods'
    
    goodid = db.Column(db.Integer, primary_key=True)
    goodname = db.Column(db.String(64),nullable = False)
    goodunit = db.Column(db.String(64),unique=False)
    goodmodel = db.Column(db.String(64),unique=False)
    inoutgood = db.relationship('InOut', backref='good')
    inoutnumber = db.relationship('Number', backref='good')



class Storehouse(db.Model):
    __tablename__ = 'storehouses'
    
    SHid = db.Column(db.Integer, primary_key=True)
    SHname = db.Column(db.String(64))
    inoutSH = db.relationship('InOut', backref='SH')
    inoutSH = db.relationship('Number', backref='SH')
    

class InOut(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    good_id = db.Column(db.Integer, db.ForeignKey('goods.goodid'))
    storehouse_id  = db.Column(db.Integer, db.ForeignKey('storehouses.SHid'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    changenumber = db.Column(db.Float)
    inorout = db.Column(db.Boolean)
    changedate = db.Column(db.DateTime,default=datetime.utcnow)
    
    
   
    
    




class Number(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    good_id = db.Column(db.Integer, db.ForeignKey('goods.goodid'))
    storehouse_id  = db.Column(db.Integer, db.ForeignKey('storehouses.SHid'))
    nownumber = db.Column(db.Integer)
    changedate = db.Column(db.DateTime,default=datetime.utcnow)
    
  

