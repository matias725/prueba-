"""
WSGI config para AWS Lambda + Zappa
"""

import os
import django
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monitoreo.settings')

# Initialize Django
django.setup()

# Get WSGI application
application = get_wsgi_application()

# Para Zappa
from zappa.middleware import ZappaMiddleware
application = ZappaMiddleware(application)
