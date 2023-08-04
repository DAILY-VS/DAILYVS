from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("vote.urls")),
<<<<<<< HEAD
    path("account/", include("account.urls")),
=======
    #path("", include("account.urls")),
>>>>>>> 9a582c9e1128f8d07e4d79aa1a98a5100133c0dd
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
