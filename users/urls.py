from django.urls import path
from . import views

urlpatterns = [
    path('linkAccount/', views.LinkAccount.as_view(), name='linkaccount'),
    path('verifyAccount/', views.VerifyAccount.as_view(), name='verifyaccount'),
    path('getVerifiedAccounts/', views.GetVerifiedAccounts.as_view(), name='getVerifiedAccounts'),

]
