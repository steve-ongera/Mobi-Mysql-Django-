from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('deposit/', views.deposit, name='deposit'),
    path('withdraw/', views.withdraw, name='withdraw'),
    path('send_money/', views.send_money, name='send_money'),
    path('register/', views.register, name='register'), # Register view
    path('login/', views.custom_login, name='login'),     # Login view
    path('logout/', views.custom_logout, name='logout'), # Logout view  
    path('account_details/', views.account_details, name='account_details'),
    path('transact/', views.transact, name='transact'),
    path('search/', views.search, name='search'),

    path('deposit-funds/', views.deposit_funds, name='deposit_funds'),
    path('withdraw-funds/', views.withdraw_funds, name='withdraw_funds'),
    path('lock-funds/', views.lock_funds, name='lock_funds'),
    path('create-mshwari-account/', views.create_mshwari_account, name='create_mshwari_account'),
]
