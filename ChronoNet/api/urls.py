from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from api import views

#The URLs for each of the views in the API
urlpatterns = [
    path('posts/', views.PostExplore.as_view()),
    path('posts/create/', views.PostCreate.as_view()),
    path('posts/feed/', views.PostFeed.as_view()),
    path('posts/<int:pk>/vote/', views.PostVote.as_view()),
    path('posts/<int:pk>/', views.PostView.as_view()),
    path('users/create/', views.UserCreate.as_view()),
    path('users/<int:pk>/follow/', views.UserFollow.as_view()),
    path('users/<int:pk>/', views.UserView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)