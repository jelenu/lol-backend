from django.contrib import admin
from django.urls import path
from accounts.views import AccountInfo
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/accounts/info/', AccountInfo.as_view(), name='third_party_api_proxy'),
]
