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
