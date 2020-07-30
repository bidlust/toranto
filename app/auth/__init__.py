#!/usr/bin/env python3
# by dongchao <cookie@maxcale.cn>

from flask import Blueprint


auth = Blueprint('auth', __name__, template_folder='pages', url_prefix='/auth')

from .views import *
