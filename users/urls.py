from django.urls import path
from . import views

urlpatterns = [
    path('linkAccount/', views.LinkAccountView.as_view(), name='linkaccount'),
    path('verifyAccount/', views.VerifyAccountView.as_view(), name='verifyaccount'),
    path('getVerifiedAccounts/', views.GetVerifiedAccountsView.as_view(), name='getVerifiedAccounts'),

    path('followSummoner/', views.FollowSummonerView.as_view(), name='followSummoner'),
    path('getfollowedSummoner/', views.GetFollowedSummonersView.as_view(), name='getfollowedSummoner'),

    path('friendRequest/', views.FriendRequestView.as_view(), name='FriendRequest'),
    path('friendRequestRecived/', views.FriendRequestRecivedView.as_view(), name='FriendRequestRecived'),
    path('friendRequestList/', views.FriendRequestsListView.as_view(), name='FriendRequestList'),
    path('friendsList/', views.FriendsListView.as_view(), name='FriendList'),


]
