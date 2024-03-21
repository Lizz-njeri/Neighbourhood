
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include ('neighbourhood.urls')),
    path('tinymce/', include('tinymce.urls')),
]  

urlpatterns+= staticfiles_urlpatterns()
