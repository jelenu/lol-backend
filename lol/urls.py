from django.contrib import admin
from django.urls import path, include
from summoners.views import AccountInfo
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/summoners/', include('summoners.urls')),
    path('api/builds/', include('builds.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)