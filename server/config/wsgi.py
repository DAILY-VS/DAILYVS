import os
import site #추가된거
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
site.addsitedir(os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))) #추가된거 각 위치경로마다 다름
application = get_wsgi_application()
