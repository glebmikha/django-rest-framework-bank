
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from bank.models import Action, Account

from bank.serializers import ActionSerializer

ACTION_URL = reverse('bank:action-list')


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
        res = self.client.get(ACTION_URL)
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
        self.account = sample_account(user=self.user)
        self.account.balance = 1000
        self.account.save()

    def test_retreive_actions(self):

        Action.objects.create(account=self.account,
                              amount=500)

        res = self.client.get(ACTION_URL)

        actions = Action.objects.all().order_by('-id')

        serializer = ActionSerializer(actions, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_acction_limited_to_user(self):
        user2 = get_user_model().objects.create_user(
            email='other@gleb.com',
            password='otherpass',
            username='test_1'
        )
        account2 = sample_account(user=user2)

        Action.objects.create(account=self.account,
                              amount=500)
        Action.objects.create(account=account2,
                              amount=500)

        res = self.client.get(ACTION_URL)

        actions = Action.objects.filter(account=self.account)

        serializer = ActionSerializer(actions, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data, serializer.data)

    def test_make_deposit(self):
        payload = {'account': self.account.id,
                   'amount': 100}

        balance_before = self.account.balance

        res = self.client.post(ACTION_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        self.account.refresh_from_db()

        balance_after = self.account.balance

        self.assertEqual(payload['amount'], balance_after - balance_before)

        action = Action.objects.get(id=res.data['id'])

        self.assertEqual(payload['account'], action.account.id)
        self.assertEqual(payload['amount'], action.amount)

    def test_make_withdraw(self):
        payload = {'account': self.account.id,
                   'amount': -100}

        self.account.balance = 1000
        self.account.save()
        balance_before = self.account.balance

        res = self.client.post(ACTION_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        self.account.refresh_from_db()

        balance_after = self.account.balance

        self.assertEqual(payload['amount'], balance_after - balance_before)

        action = Action.objects.get(id=res.data['id'])

        self.assertEqual(payload['account'], action.account.id)
        self.assertEqual(payload['amount'], action.amount)

    def test_make_withdraw_with_not_enough_money(self):
        payload = {'account': self.account.id,
                   'amount': -100}

        self.account.balance = 0
        self.account.save()

        res = self.client.post(ACTION_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_listing_actions_from_several_accounts(self):
        account2 = sample_account(user=self.user)

        Action.objects.create(account=self.account,
                              amount=500)
        Action.objects.create(account=account2,
                              amount=500)

        res = self.client.get(ACTION_URL)

        self.assertEqual(len(res.data), 2)
