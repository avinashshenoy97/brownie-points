from django.urls import path
from . import views

urlpatterns = [
    path('', views.wallet, name='wallet'),
    path('sendCoins',views.sendCoinsView.as_view()),
    path('getTransactionDetails',views.transactionStatusView.as_view()),
    path('getPublicAddress',views.publicAddressView.as_view()),
    path('getBalance',views.balanceView.as_view())
]