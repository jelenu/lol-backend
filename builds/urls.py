from django.urls import path
from . import views

urlpatterns = [
    path('items/all/', views.TagStatItemView.as_view(), name='item-list'),
    path('match/runes/', views.TagStatItemView.as_view(), name='item-list'),

]
