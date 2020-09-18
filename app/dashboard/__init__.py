#!/usr/bin/env python3
# by dongchao <cookie@maxcale.cn>

from flask import Blueprint

dashboard = Blueprint('dashboard', __name__, template_folder='pages', url_prefix='/auth')

from . import views