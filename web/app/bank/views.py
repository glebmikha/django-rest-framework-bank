from .serializers import (CustomerSerializer, AccountSerializer,
                          ActionSerializer, TransactionSerializer,
                          TransferSerializer)
from .models import Customer, Account, Action, Transaction, Transfer
from rest_framework import generics, viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .services import make_transfer, filter_user_account, check_account_exists
from .mixins import ServiceExceptionHandlerMixin
from rest_framework.views import APIView


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


class AccountViewSet(viewsets.GenericViewSet,
                     mixins.ListModelMixin,
                     mixins.CreateModelMixin):
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


class ActionViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin,
                    mixins.CreateModelMixin):
    serializer_class = ActionSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, )
    queryset = Action.objects.all()

    def get_queryset(self):
        """Return object for current authenticated user only"""
        # get account of user
        accounts = Account.objects.filter(user=self.request.user)
        return self.queryset.filter(account__in=accounts)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # check if requested account belongs to user

        try:
            account = Account.objects.filter(
                user=self.request.user).get(pk=self.request.data['account'])
        except Exception as e:
            print(e)
            content = {'error': 'No such account'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        serializer.save(account=account)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED,
                        headers=headers)


class TransactionViewSet(viewsets.GenericViewSet,
                         mixins.ListModelMixin,
                         mixins.CreateModelMixin,
                         mixins.RetrieveModelMixin):
    serializer_class = TransactionSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, )
    queryset = Transaction.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        try:
            account = Account.objects.filter(
                user=self.request.user).get(pk=self.request.data['account'])
        except Exception as e:
            print(e)
            content = {'error': 'No such account'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        serializer.save(account=account)

        try:
            Transaction.make_transaction(**serializer.validated_data)
        except ValueError:
            content = {'error': 'Not enough money'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED,
                        headers=headers)

    def get_queryset(self):
        """Return object for current authenticated user only"""
        # get account of user
        accounts = Account.objects.filter(user=self.request.user)
        return self.queryset.filter(account__in=accounts)


class TransferViewSet(viewsets.GenericViewSet,
                      mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      mixins.RetrieveModelMixin,
                      ServiceExceptionHandlerMixin):

    serializer_class = TransferSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, )
    queryset = Transfer.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            make_transfer(**serializer.validated_data)
        except ValueError:
            content = {'error': 'Not enough money'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED,
                        headers=headers)

    def get_queryset(self):
        """Return object for current authenticated user only"""
        # filter accounts by user
        accounts = Account.objects.filter(user=self.request.user)
        return self.queryset.filter(from_account__in=accounts)


class CreateTransferView(
    ServiceExceptionHandlerMixin,
    APIView
):

    # if i do create this way I don't have to handle exception manualy
    # ServiceExceptionHandlerMixin do it for me

    serializer_class = TransferSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, )
    queryset = Transfer.objects.all()

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)

        from_account = filter_user_account(
            self.request.user,
            self.request.data['from_account'])

        to_account = check_account_exists(self.request.data['to_account'])

        make_transfer(
            from_account,
            to_account,
            float(self.request.data['amount']))

        return Response(serializer.data, status=status.HTTP_201_CREATED)
