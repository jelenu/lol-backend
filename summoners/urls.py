from django.urls import path
from . import views

urlpatterns = [
    path('info/', views.AccountInfoView.as_view(), name='get_account_info'),
    path('matches/id/', views.MatchIdView.as_view(), name='get_matches_info'),
    path('matches/info/', views.MatchInfoView.as_view(), name='get_matches_info'),
    path('matches/timeline/', views.MatchTimeLineView.as_view(), name='get_match_timeline'),



]
