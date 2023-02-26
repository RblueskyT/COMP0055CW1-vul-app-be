from django.urls import path
from . import views

urlpatterns = [
    # /login/
    path('', views.index, name='index'),
    # /login/github_login/
    path('github_login', views.github_login, name='github_login'),
    # /login/twitter_login/
    path('twitter_login', views.twitter_login, name='twitter_login'),
    path('tweet', views.tweet, name='tweet'),
] 