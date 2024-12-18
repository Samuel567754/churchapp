from django.contrib import admin
from django.urls import path, include
# from django.conf.urls import url

from django.conf import settings
from django.conf.urls.static import static
import os
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls), 
    path('', include('community.urls')), 
    path('blog/', include('blog.urls')),
    path('worship/', include('worship.urls')),  
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


