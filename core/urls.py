from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('deposit/', views.deposit, name='deposit'),
    path('withdraw/', views.withdraw, name='withdraw'),
    path('send_money/', views.send_money, name='send_money'),
    path('register/', views.register, name='register'), # Register view
    path('login/', views.custom_login, name='login'),     # Login view
    path('logout/', views.custom_logout, name='logout'), # Logout view  transact
    path('account_details/', views.account_details, name='account_details'),
    path('transact/', views.transact, name='transact'),
]
