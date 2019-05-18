from bank.services import make_interest

from django.contrib.auth import get_user_model
from django.test import TestCase


from bank.models import Account, Interest


def sample_account(user, **params):
    """Create and return a sample customer"""
    defaults = {}
    defaults.update(params)

    return Account.objects.create(user=user, **defaults)


class TestServices(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='test@londonappdev.com',
            password='testpass',
            username='test'
        )

        self.account = sample_account(user=self.user)
        self.account.balance = 1000
        self.account.save()

    def test_make_interest(self):

        balance_before = self.account.balance
        target_interest = balance_before * 0.08 / 12
        target_balance = balance_before + target_interest

        make_interest()

        interests = Interest.objects.all()

        self.account.refresh_from_db()

        self.assertEqual(len(interests), 1)
        self.assertEqual(round(target_interest, 2), float(interests[0].amount))
        self.assertEqual(round(target_balance, 2), float(self.account.balance))
