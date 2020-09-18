#!/usr/bin/env python3
# by dongchao <cookie@maxcale.cn>

#!/usr/bin/env python3

from .default import Default
from .develop import Develop
from .product import Product
import os

def get_config( envName ):

    if envName == 'dev':
        return Develop()
    elif envName == 'prd':
        return Product()
    else:
        return Default()
