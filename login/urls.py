from django.urls import path
from . import views

urlpatterns = [
    # /login/account_login/
    path('account_login', views.account_login, name='account_login'),
    # /login/github_client_flow_redeem/
    path('github_client_flow_redeem', views.github_client_flow_redeem, name='github_client_flow_redeem'),
    # /login/github_client_flow_login/
    path('github_client_flow_login', views.github_client_flow_login, name='github_client_flow_login'),
    # /login/github_server_flow_info/
    path('github_server_flow_info', views.github_server_flow_info, name='github_server_flow_info'),
    # /login/github_server_flow_redeem_and_login/
    path('github_server_flow_redeem_and_login', views.github_server_flow_redeem_and_login, name='github_server_flow_redeem_and_login'),
    # /login/twitter_server_flow_info/
    path('twitter_server_flow_info', views.twitter_server_flow_info, name='twitter_server_flow_info'),
    # /login/twitter_server_flow_redeem_and_login/
    path('twitter_server_flow_redeem_and_login', views.twitter_server_flow_redeem_and_login, name='twitter_server_flow_redeem_and_login'),
    # /login/dropbox_server_flow_info/
    path('dropbox_server_flow_info', views.dropbox_server_flow_info, name='dropbox_server_flow_info'),
    # /login/dropbox_server_flow_redeem_and_login/
    path('dropbox_server_flow_redeem_and_login', views.dropbox_server_flow_redeem_and_login, name='dropbox_server_flow_redeem_and_login'),
    # /login/user_logout/
    path('user_logout', views.user_logout, name='user_logout'),
    # /login/check_user_status/
    path('check_user_status', views.check_user_status, name='check_user_status'),
] 