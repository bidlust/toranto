#!/usr/bin/env python3
# by dongchao <cookie@maxcale.cn>

from sqlalchemy import Column, Integer,SmallInteger, Text, Boolean, String, CHAR, DateTime, DECIMAL
from sqlalchemy import UniqueConstraint, Index
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.sql import func
from . import db

class User(db.Model):

    __tablename__ = 'user'
    __table_args__ = {
        'mysql_engine' : 'InnoDB',
        'mysql_charset' : 'utf8mb4',
        'mysql_collate': 'utf8mb4_unicode_ci'
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
        'mysql_charset': 'utf8mb4',
        'mysql_collate': 'utf8mb4_unicode_ci'
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
        'mysql_charset': 'utf8mb4',
        'mysql_collate': 'utf8mb4_unicode_ci'
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
        'mysql_charset': 'utf8mb4',
        'mysql_collate': 'utf8mb4_unicode_ci'
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
        'mysql_charset': 'utf8mb4',
        'mysql_collate': 'utf8mb4_unicode_ci'
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
        'mysql_charset': 'utf8mb4',
        'mysql_collate': 'utf8mb4_unicode_ci'
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
        'mysql_charset': 'utf8mb4',
        'mysql_collate': 'utf8mb4_unicode_ci'
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



class  Article(db.Model):
    __tablename__ = 'toranto_article'
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4',
        'mysql_collate': 'utf8mb4_unicode_ci'
    }

    id = Column(Integer, primary_key=True, autoincrement=True)
    article_category = Column(String(255), nullable=True)
    article_title = Column(String(255), nullable=False)
    article_author = Column(String(255), nullable=False)
    article_desc = Column(Text, nullable=True)
    article_content = Column(Text, nullable=False)
    article_tag = Column(String(255), nullable=True)
    article_click = Column(Integer, nullable=False, server_default='1')
    article_praise =  Column(Integer, nullable=False, server_default='2')
    article_step = Column(Integer, nullable=False, server_default='1')
    article_seo = Column(String(255), nullable=True)
    article_picture = Column(String(255), nullable=True)
    article_password = Column(String(255), nullable=True)
    article_price = Column(DECIMAL(10,2), nullable=True)
    sq = Column(Integer, nullable=False, server_default='1')
    top = Column(Integer, nullable=False, server_default='1')
    iscomment = Column(CHAR(1), nullable=False, server_default='1')
    ispublish = Column(CHAR(1), nullable=False, server_default='1')
    isvisible = Column(CHAR(1), nullable=False, server_default='1')
    istoolbar = Column(CHAR(1), nullable=False, server_default='1')
    date_expire = Column(DateTime, nullable=False, server_default='2120-01-01 00:00:00')
    valid = Column(CHAR(1), nullable=False, server_default='1')
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime, nullable=True)




class Attachment(db.Model):
    __tablename__ = 'toranto_attachment'
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4',
        'mysql_collate': 'utf8mb4_unicode_ci'
    }
    id                  = Column(Integer, primary_key=True, autoincrement=True)
    attach_article_title   = Column(String(255), nullable=False)
    attach_name         = Column(String(255), nullable=False)
    attach_saved        = Column(String(255), nullable=False)
    attach_upload_path  = Column(String(255), nullable=False)
    attach_type         = Column(String(255), nullable=False)
    attach_size         = Column(Integer, default=0)
    attach_visit        = Column(String(255), nullable=True)
    attach_creator      = Column(String(255), nullable=True)
    attach_password     = Column(String(255), nullable=True)
    attach_price        = Column(DECIMAL(10,2), nullable=True)
    valid               = Column(CHAR(1), nullable=False, server_default='0')
    created_at          = Column(DateTime, nullable=False, server_default=func.now())
    updated_at          = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
    deleted_at          = Column(DateTime, nullable=True)


class Category(db.Model):
    __tablename__ = 'toranto_category'
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4',
        'mysql_collate': 'utf8mb4_unicode_ci'
    }

    id = Column(Integer, primary_key=True, autoincrement=True)
    category_name = Column(String(255), nullable=False)
    category_desc = Column(String(2048), nullable=True)
    category_creator = Column(String(2048), nullable=True, default="admin")
    valid = Column(CHAR(1), nullable=False, server_default='1')
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime, nullable=True)


class Link(db.Model):
    __tablename__ = 'toranto_link'
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4',
        'mysql_collate': 'utf8mb4_unicode_ci'
    }
    id = Column(Integer, primary_key=True, autoincrement=True)
    link_name = Column(String(255), nullable=False)
    link_href = Column(String(255), nullable=False)
    link_desc = Column(String(2048), nullable=True)
    link_creator = Column(String(255), nullable=False)
    link_from = Column(String(255), nullable=True)
    link_field = Column(String(255), nullable=True)
    valid = Column(CHAR(1), nullable=False, server_default='0')
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime, nullable=True)


class Industry(db.Model):
    __tablename__ = 'toranto_industry'
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4',
        'mysql_collate': 'utf8mb4_unicode_ci'
    }
    id = Column(Integer, primary_key=True, autoincrement=True)
    industry_name =  Column(String(255), nullable=False)
    valid = Column(CHAR(1), nullable=False, server_default='1')
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime, nullable=True)


    def __init__(self, **kwargs):
        self.industry_name = kwargs.get('industry_name')


class Share(db.Model):
    __tablename__ = 'toranto_share'
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4',
        'mysql_collate': 'utf8mb4_unicode_ci'
    }
    id = Column(Integer, primary_key=True, autoincrement=True)
    share_name = Column(String(255), nullable=False)
    share_desc = Column(Text, nullable=True)
    share_click = Column(Integer, default=1)
    share_download = Column(Integer, default=1)
    share_creator = Column(String(255), nullable=True)
    share_type = Column(String(255), nullable=False, default='PDF')
    share_location = Column(String(255), nullable=False, default='local')
    share_link = Column(String(255), nullable=False)
    share_password = Column(String(255), nullable=True)
    share_price = Column(DECIMAL(10,2), nullable=True)
    iscomment = Column(CHAR(1), nullable=False, server_default='1')
    valid = Column(CHAR(1), nullable=False, server_default='1')
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime, nullable=True)


class Uploadfile(db.Model):
    __tablename__ = 'toranto_upload'
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4',
        'mysql_collate': 'utf8mb4_unicode_ci'
    }
    id = Column(Integer, primary_key=True, autoincrement=True)
    upload_name     =  Column(String(255), nullable=False)
    upload_path     = Column(String(255), nullable=False)
    upload_type     = Column(String(255), nullable=False)
    upload_size     = Column(Integer, default=0)
    upload_busi     = Column(String(255), nullable=True)
    upload_real     = Column(String(255), nullable=True)
    upload_saved    = Column(String(255), nullable=True)
    upload_visit    = Column(String(255), nullable=True)
    upload_creator  = Column(String(255), nullable=True)
    valid           = Column(CHAR(1), nullable=False, server_default='1')
    created_at      = Column(DateTime, nullable=False, server_default=func.now())
    updated_at      = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
    deleted_at      = Column(DateTime, nullable=True)


class Pwdmap(db.Model):
    __tablename__ = 'toranto_pwdmap'
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4',
        'mysql_collate': 'utf8mb4_unicode_ci'
    }
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    pwd = Column(String(255), nullable=False)
    valid = Column(CHAR(1), nullable=False, server_default='1')
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime, nullable=True)


