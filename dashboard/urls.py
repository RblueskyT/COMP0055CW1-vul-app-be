from django.urls import path
from . import views

urlpatterns = [
    # /dashboard/tweet/
    path('tweet', views.tweet, name='tweet'),
    # /dashboard/get_user_balance/
    path('get_user_balance', views.get_user_balance, name='get_user_balance'),
    # /dashboard/get_user_balance_records/
    path('get_user_balance_records', views.get_user_balance_records, name='get_user_balance_records'),
    # /dashboard/account_transfer/
    path('account_transfer', views.account_transfer, name='account_transfer'),
    # /dashboard/get_posts/
    path('get_posts', views.get_posts, name='get_posts'),
    # /dashboard/add_post/
    path('add_post', views.add_post, name='add_post'),
] 