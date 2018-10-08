from django.urls import path
from . import views

urlpatterns = [
    path('wallet/', views.wallet, name='wallet'),
    path('wallet/sendCoins',views.sendCoinsView.as_view()),
    path('wallet/getTransactionDetails',views.transactionStatusView.as_view()),
    path('wallet/getPublicAddress',views.publicAddressView.as_view()),
    path('wallet/getBalance',views.balanceView.as_view())
]