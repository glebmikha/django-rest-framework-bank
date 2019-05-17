from rest_framework.routers import DefaultRouter
from django.urls import path, include
from bank import views

# from rest_framework.urlpatterns import format_suffix_patterns

app_name = 'bank'

router = DefaultRouter()

router.register('acustomer', views.CustomerDetail2)
router.register('account', views.AccountViewSet)
router.register('action', views.ActionViewSet)
router.register('transaction', views.TransactionViewSet)
router.register('transfer', views.TransferViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('customer/', views.CustomerDetail3.as_view(), name='customer'),
    path('transfer_alt/', views.CreateTransferView.as_view())
]

# not working with routes. I thing because this is included in routes
# urlpatterns = format_suffix_patterns(urlpatterns)
