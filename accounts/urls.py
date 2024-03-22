from django.urls import path
from . import views

urlpatterns = [
    path('info/', views.AccountInfo.as_view(), name='get_account_info'),
    path('matches/', views.MatchInfo.as_view(), name='get_matches_info'),

]
