from django.urls import path
from . import views

urlpatterns = [
    # /login/
    path('', views.index, name='index'),
    # /login/account_login/
    path('account_login', views.account_login, name='account_login'),
    # /login/github_client_flow_redeem/
    path('github_client_flow_redeem', views.github_client_flow_redeem, name='github_client_flow_redeem'),
    # /login/github_client_flow_login/
    path('github_client_flow_login', views.github_client_flow_login, name='github_client_flow_login'),
    # /login/user_logout
    path('user_logout', views.user_logout, name='user_logout'),
    # /login/check_user_status/
    path('check_user_status', views.check_user_status, name='check_user_status'),
    # /login/github_login/
    path('github_login', views.github_login, name='github_login'),
    # /login/twitter_login/
    path('twitter_login', views.twitter_login, name='twitter_login'),
    path('tweet', views.tweet, name='tweet'),
] 