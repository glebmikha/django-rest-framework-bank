from rest_framework.routers import DefaultRouter
from django.urls import path, include
from bank import views

from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

app_name = 'bank'

# urlpatterns = [
#     path('customer/', views.CustomerDetail2, name='customer'),
#     # path('customer/<int:pk>/', views.CustomerDetail.as_view()),
# ]

# urlpatterns = format_suffix_patterns(urlpatterns)


router = DefaultRouter()

router.register('customer', views.CustomerDetail2)


urlpatterns = [
    path('', include(router.urls))
]
