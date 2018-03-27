import sys
import os
import django

sys.path.append('/home/vu/vuDJANGOproject/mysite')
# sys.path.append('/home/vu/vuDJANGOproject/mysite/mysite')

os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'

django.setup()

from django.conf import settings

