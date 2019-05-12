
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from bank.models import Account

from bank.serializers import AccountSerializer

ACCOUNT_URL = reverse('bank:account-list')


def sample_account(user, **params):
    """Create and return a sample customer"""
    defaults = {}
    defaults.update(params)

    return Account.objects.create(user=user, **defaults)


class PublicBankApiTest(TestCase):
    """Test unauthenticated recipe API request"""

    def setUp(self):
        self.client = APIClient()

    def test_account_auth_required(self):
        res = self.client.get(ACCOUNT_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateCustomerApiTests(TestCase):
    """Test authenticated API access"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='test@londonappdev.com',
            password='testpass',
            username='test'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retreive_account(self):
        sample_account(user=self.user)

        res = self.client.get(ACCOUNT_URL)

        account = Account.objects.all().order_by('-id')

        serializer = AccountSerializer(account, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_account_limited_to_user(self):
        user2 = get_user_model().objects.create_user(
            email='other@gleb.com',
            password='otherpass',
            username='test_1'
        )
        sample_account(user=user2)
        sample_account(user=self.user)

        res = self.client.get(ACCOUNT_URL)

        accounts = Account.objects.filter(user=self.user)

        serializer = AccountSerializer(accounts, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data, serializer.data)

    def test_create_account(self):
        payload = {}
        res = self.client.post(ACCOUNT_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        account = Account.objects.get(id=res.data['id'])
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(account, key))

    def test_create_account_always_zero(self):
        payload = {'balance': 20000.232}
        res = self.client.post(ACCOUNT_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        account = Account.objects.get(id=res.data['id'])
        self.assertEqual(0, account.balance)

    def test_partial_update_account(self):

        account = sample_account(user=self.user)
        url = ACCOUNT_URL + str(account.id) + '/'

        payload = {
            'balance': 9999999
        }

        res = self.client.patch(url, payload)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

        res = self.client.patch(ACCOUNT_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_full_update_account(self):
        account = sample_account(user=self.user)
        url = ACCOUNT_URL + str(account.id) + '/'

        payload = {
            'balance': 9999999
        }

        res = self.client.put(url, payload)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

        res = self.client.put(ACCOUNT_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
