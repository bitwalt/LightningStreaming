""" Production Settings """

import os
# import dj_database_url
from .dev import *


############
# DATABASE #
############
# DATABASES = {
#     'default': dj_database_url.config(
#         default=os.getenv('DATABASE_URL')
#     )
# }


############
# SECURITY #
############

DEBUG = False # bool(os.getenv('DJANGO_DEBUG', ''))

# Set to your Domain here (eg. 'yourwebsite.com')
ALLOWED_HOSTS = ['*']
