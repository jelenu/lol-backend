from django.urls import path
from . import views

urlpatterns = [
    path('linkAccount/', views.LinkAccount.as_view(), name='linkaccount'),
    path('verifyAccount/', views.VerifyAccount.as_view(), name='verifyaccount'),
]
