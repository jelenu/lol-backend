from django.contrib import admin
from django.urls import path
from accounts.views import AccountInfo
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/accounts/info/', AccountInfo.as_view(), name='third_party_api_proxy'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)