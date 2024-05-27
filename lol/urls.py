from django.contrib import admin
from django.urls import path, include, re_path
from summoners.views import AccountInfo
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/summoners/', include('summoners.urls')),
    path('api/builds/', include('builds.urls')),

    re_path(r'^auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.jwt')),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)