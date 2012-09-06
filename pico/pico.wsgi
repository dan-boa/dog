import sys
import os
ROOT_DIR = '/home/dan/Goibibo-Lab/django-dog/'
sys.stdout = sys.stderr # sys.stdout access restricted by mod_wsgi
path = ROOT_DIR # import pico from this dir
path1 = ROOT_DIR + "pico/" # import pico from this dir
sys.path.insert(0, path)
sys.path.insert(0, path1)

import pico.server

# Set the WSGI application handler
application = pico.server.wsgi_app

