"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from . import views

#All of the urls that have to do with posts
urlpatterns = [
    path('new/', views.PostCreateView.as_view(), name='create_post'),   
    path('vote/', views.makeVote, name='make_vote'),
    path('posts/time', views.getPostsTime, name='get_posts_time'),
    path('explore/', views.postListViewExplore, name='explore'),
    path('feed/', views.postListViewUserFeed, name='feed'),
    path('delete/', views.deletePost, name='delete_post'),
]
