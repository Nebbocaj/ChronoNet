from django.urls import path
from . import views

urlpatterns = [
    # User Urls
    path('userProfile/',views.userProfile, name='userProfile'),
    path('userFriends/',views.userFriends, name='userFriends'),
    path('userFeed/',views.userFeed, name='userFeed'),
    path('userExplore/',views.userExplore, name='userExplore'),
    path('userSearch/',views.userSearch, name='userSearch'),
]