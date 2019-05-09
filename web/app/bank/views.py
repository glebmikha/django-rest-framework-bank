from .serializers import CustomerSerializer, AccountSerializer
from .models import Customer, Account

from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets


class CustomerList(generics.ListCreateAPIView):
    """Get a list, put and patch are not allowed"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    def get_queryset(self):
        """Return object for current authenticated user only"""
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Create a new attribue"""
        serializer.save(user=self.request.user)


class CustomerDetail(generics.RetrieveUpdateAPIView):
    """Detail. to put and patch pk should be in urls"""
    serializer_class = CustomerSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, )
    queryset = Customer.objects.all()

    def get_queryset(self):
        """Return object for current authenticated user only"""
        return self.queryset.filter(user=self.request.user)


class CustomerDetail2(viewsets.ModelViewSet):
    """Example of view set. Put and patch avalible only via pk
    and urls should be configured via routes"""
    serializer_class = CustomerSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, )
    queryset = Customer.objects.all()

    def perform_create(self, serializer):
        """Create a new customer"""
        serializer.save(user=self.request.user)

    def get_queryset(self):
        """Return object for current authenticated user only"""
        return self.queryset.filter(user=self.request.user)


class CustomerDetail3(generics.RetrieveUpdateAPIView):
    """Single end point for get and put, no pk needed, auth user is used
    for filter. Put works as create!!! You don't even need to add createmodel
    mixin.
    """
    serializer_class = CustomerSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, )
    queryset = Customer.objects.all()

    def get_object(self):
        return self.queryset.filter(user=self.request.user).first()


class AccountViewSet(viewsets.ModelViewSet):
    serializer_class = AccountSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, )
    queryset = Account.objects.all()

    def perform_create(self, serializer):
        """Create a new account"""
        serializer.save(user=self.request.user)

    def get_queryset(self):
        """Return object for current authenticated user only"""
        return self.queryset.filter(user=self.request.user)
