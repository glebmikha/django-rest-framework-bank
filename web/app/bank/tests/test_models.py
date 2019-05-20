from django.test import TestCase
from django.contrib.auth import get_user_model
from unittest.mock import patch

from bank import models


def sample_user(email='test@test.com', password='testpass'):
    """Create a sample user"""
    return get_user_model().objects.create_user(email, password)


class ModelTest(TestCase):

    def test_customer_str(self):
        """Test the customer string representation"""
        customer = models.Customer.objects.create(
            user=sample_user(),
            fname='Jon',
            lname='Snow',
            city='Winterfell',
            house='Stark'
        )

        self.assertEqual(str(customer), f'{customer.fname} {customer.lname}')

    @patch('uuid.uuid4')
    def test_customer_file_name_uuid(self, mock_uuid):
        """Test that the image is saved in the correct location"""
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = models.customer_image_file_path(None, 'myimage.jpg')

        exp_path = f'upload/customer/{uuid}.jpg'

        self.assertEqual(file_path, exp_path)

    def test_account_str(self):
        """Test the customer string representation"""

        test_user = sample_user()

        account1 = models.Account.objects.create(
            user=test_user,
        )

        account2 = models.Account.objects.create(
            user=test_user,
            balance=2000.32
        )

        self.assertEqual(str(account1), '1 of test@test.com')
        self.assertEqual(str(account2), '2 of test@test.com')

    def test_action_str(self):
        """Test the action string representation"""

        test_user = sample_user()

        account = models.Account.objects.create(
            user=test_user,
        )

        account_id = account.id

        action1 = models.Action.objects.create(
            amount=1000,
            account=account
        )

        self.assertEqual(
            str(action1), f'Account number {account_id} was changed on 1000')

    def test_make_transaction_success(self):
        """Make succesful transaction"""
        test_user = sample_user()

        initial_balance = 1000
        trans_amount = 500

        account = models.Account.objects.create(
            user=test_user,
            balance=initial_balance
        )

        models.Transaction.make_transaction(
            account=account,
            amount=trans_amount,
            merchant='bk'
        )

        account.refresh_from_db()

        expected_balance = initial_balance - trans_amount

        transactions = models.Transaction.objects.all()

        self.assertEqual(expected_balance, account.balance)
        self.assertEqual(len(transactions), 1)

    def test_make_transaction_failed(self):
        """Make failed transaction"""
        test_user = sample_user()

        initial_balance = 1000
        trans_amount = 1500

        account = models.Account.objects.create(
            user=test_user,
            balance=initial_balance
        )

        try:
            models.Transaction.make_transaction(
                account=account,
                amount=trans_amount,
                merchant='bk'
            )
        except ValueError:
            pass
        else:
            raise AssertionError("ValueError was not raised")
