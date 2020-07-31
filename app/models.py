#!/usr/bin/env python3
# by dongchao <cookie@maxcale.cn>

from sqlalchemy import Column, Integer,SmallInteger, Text,Boolean, String, CHAR, DateTime
from sqlalchemy import UniqueConstraint, Index
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.sql import func
from . import db

class User(db.Model):

    __tablename__ = 'user'
    __table_args__ = {
        'mysql_engine' : 'InnoDB',
        'mysql_charset' : 'utf8',
        'mysql_collate': 'utf8_unicode_ci'
    }

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(255), nullable=False, unique=True)
    email = Column(String(255), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)
    profile = Column(String(255), nullable=True)
    remark = Column(String(255), nullable=True)
    ip = Column(String(255), nullable=True)
    active = Column(CHAR(1), nullable=False, server_default='1')
    valid = Column(CHAR(1), nullable=False, server_default='1')
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())


    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute')

    @password.setter
    def password(self, pwd):
        self.password_hash = generate_password_hash(pwd)

    def check_password(self, pwd):
        return check_password_hash(self.password_hash, pwd)

    def __init__(self, **kwargs):
        self.username = kwargs.get('username')
        self.password_hash = kwargs.get('password')
        self.email = kwargs.get('email')
        self.profile = kwargs.get('profile')
        self.ip = kwargs.get('ip')

    def __repr__(self):
        return "<User(name='%s', email='%s')>" % (self.username, self.email)


class Role(db.Model):
    __tablename__ = 'role'
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8',
        'mysql_collate': 'utf8_unicode_ci'
    }

    id = Column(Integer, primary_key=True, autoincrement=True)
    role = Column(String(255), nullable=False, unique=True)
    desc = Column(String(255), nullable=True)
    valid = Column(CHAR(1), nullable=False, server_default='1')
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    def __init__(self, **kwargs):
        self.role = kwargs.get('role')
        self.desc = kwargs.get('desc') or None

    def __repr__(self):
        return "<Role(name='%s', desc='%s')>" % (self.role, self.desc)

class UserRoleMap(db.Model):
    __tablename__ = 'user_role_map'
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8',
        'mysql_collate': 'utf8_unicode_ci'
    }

    id = Column(Integer, primary_key=True, autoincrement=True)
    user = Column(String(255), nullable=True)
    role = Column(String(255), nullable=True)
    valid = Column(CHAR(1), nullable=False, server_default='1')
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())


class Modules(db.Model):
    __tablename__ = 'module'
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8',
        'mysql_collate': 'utf8_unicode_ci'
    }

    id          = Column(Integer, primary_key=True, autoincrement=True)
    parentId    = Column(Integer, nullable=False)
    level       = Column(Integer, nullable=False)
    sq          = Column(SmallInteger, nullable=False, server_default='1')
    action      = Column(String(255), nullable=False, unique=True)
    cname       = Column(String(255), nullable=False, unique=True)
    ename       =  Column(String(255), nullable=True, unique=True)
    icon        = Column(String(255), nullable=True)
    valid       = Column(CHAR(1), nullable=False, server_default='1')
    created_at  = Column(DateTime, nullable=False, server_default=func.now())
    updated_at  = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

class RoleModuleMap(db.Model):
    __tablename__ = 'role_module'
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8',
        'mysql_collate': 'utf8_unicode_ci'
    }

    id = Column(Integer, primary_key=True, autoincrement=True)
    role = Column(String(255), nullable=False)
    module = Column(String(255), nullable=False)
    valid = Column(CHAR(1), nullable=False, server_default='1')
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

class LoginHistory(db.Model):
    __tablename__ = 'login_history'
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8',
        'mysql_collate': 'utf8_unicode_ci'
    }

    id          = Column(Integer, primary_key=True, autoincrement=True)
    username    =  Column(String(255), nullable=False)
    ip          =  Column(String(255), nullable=False, server_default='UNKNOWN')
    created_at  = Column(DateTime, nullable=False, server_default=func.now())

    def __init__(self, **kwargs):
        self.username = kwargs.get('username')
        self.ip = kwargs.get('ip')

class TorantoSetting(db.Model):
    __tablename__ = 'toranto_setting'
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8',
        'mysql_collate': 'utf8_unicode_ci'
    }

    id = Column(Integer, primary_key=True, autoincrement=True)
    site_name = Column(String(255), nullable=False)
    site_active = Column(CHAR(1), nullable=False, server_default='1')
    site_comment = Column(CHAR(1), nullable=False, server_default='1')
    site_title = Column(String(255), nullable=True)
    site_logo = Column(String(255), nullable=True)
    site_keywords = Column(String(255), nullable=True)
    site_description = Column(Text, nullable=True)
    site_foot = Column(String(255), nullable=True)
    site_domain = Column(String(255), nullable=True)
    created_by = Column(String(255), nullable=False, unique=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    def __init__(self, **kwargs):
        self.site_name          = kwargs.get('site_name')
        self.site_active        = kwargs.get('site_active')
        self.site_comment       = kwargs.get('site_comment')
        self.site_title         = kwargs.get('site_title')
        self.site_logo          = kwargs.get('site_logo')
        self.site_keywords      = kwargs.get('site_keywords')
        self.site_description   = kwargs.get('site_description')
        self.site_foot          = kwargs.get('site_foot')
        self.site_domain        = kwargs.get('site_domain')
