from bank import views

from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [
    path('customer/', views.CustomerDetail2.as_view()),
    # path('customer/<int:pk>/', views.CustomerDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
