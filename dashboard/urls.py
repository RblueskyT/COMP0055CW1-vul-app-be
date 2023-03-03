from django.urls import path
from . import views

urlpatterns = [
    # /dashboard/get_user_balance/
    path('get_user_balance', views.get_user_balance, name='get_user_balance'),
    # /dashboard/get_user_balance_records/
    path('get_user_balance_records', views.get_user_balance_records, name='get_user_balance_records'),
    # /dashboard/account_transfer/
    path('account_transfer', views.account_transfer, name='account_transfer'),
    # /dashboard/
    path('', views.index, name='index'),
] 