import os
import site
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
site.addsitedir(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
application = get_wsgi_application()
